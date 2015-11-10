#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import traceback
from collections import deque
from utils import preprocess_line
from utils import validate_color, validate_name, validate_phonenumber_or_raise
from utils import validate_mi_or_raise, validate_zipcode_or_raise, write_json
from data_errors import data_excepthook, DataValueError

logging.basicConfig(level=logging.INFO)
sys.excepthook = data_excepthook

FIELDS = ('color', 'firstname', 'lastname', 'phonenumber', 'zipcode')
VALIDATORS = (
    validate_color, validate_name, validate_name, validate_phonenumber_or_raise,
    validate_zipcode_or_raise
)


def process_nameblock(elements):
    """
    Takes a list of elements that begins with a
    "FIRSTNAME LASTNAME" block or a "FIRSTNAME M.I.
    LASTNAME" block to [FIRSTNAME, LASTNAME, ...]
    """
    temp = deque(elements)
    nameblock = temp.popleft()
    name = nameblock.split()
    if len(name) == 3:
        validate_mi_or_raise(name[1])
        temp.extendleft([name[2], " ".join(name[:2])])
    elif len(name) == 2:
        temp.extendleft([name[1], name[0]])
    else:
        raise DataValueError("BadNameblock", nameblock)
    return list(temp)


def determine_linetype(elements):
    """
    Tests for and returns ordering for current known line types.
    line_type 0   [Lastname, Firstname, (703)-742-0996, Blue, 10013]
    line_type 1   [Firstname Lastname, Red, 11237, 703 955 0373]
    line_type 2   [Firstname, Lastname, 10013, 646 111 0101, Green]
    """
    if len(elements) == 5:
        if elements[4][0].isdigit(): # line_type 0
            indices = [3, 1, 0, 2, 4]
        else: # line_type 2
            indices = [4, 0, 1, 3, 2]
    elif len(elements) == 4: # line_type 1
        elements = process_nameblock(elements)
        indices = [2, 0, 1, 4, 3]
    else:
        raise DataValueError("BadLineElements", str(elements))
    return elements, indices


def create_entry(elements, indices):
    """
    Extracts the entry from the list of entry elements in the order
    specifed by the indices. Relies on global specifications of the
    order of fields for the entry, and for the validators for each
    field. An entry is considered invalid if its phone number does
    not contain the proper number of digits.
    """
    new_elements = [
        VALIDATORS[i](elements[indices[i]]) for i in xrange(len(FIELDS))
    ]
    entry = dict(zip(FIELDS, new_elements))
    return entry


def produce_entry(line):
    """Rule ordering function for producing a valid entry."""
    elements = preprocess_line(line)
    elements, indices = determine_linetype(elements)
    entry = create_entry(elements, indices)
    return entry


def main(filename):
    """
    Normalize each entry found in csv filename file into standard JSON.
    Write to file result.out
    """
    abspath = os.path.abspath(filename)
    with open(abspath) as infile:
        entries = []
        errors = []
        line_count = 0
        for line in infile:
            try:
                entries.append(produce_entry(line))
            except DataValueError as e:
                logging.error(e.err_type+"\t"+e.value)
                errors.append(line_count)
            finally:
                line_count += 1
    entries.sort(key=lambda x: (x['lastname'], x['firstname']))
    result = {'entries': entries, 'errors': errors}
    write_json(result, 'result.out')
    return entries


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 1:
        filename = 'data.in'
    else:
        raise SyntaxError("Too many arguments")
        sys.exit(2)
    main(filename)
