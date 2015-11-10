# -*- coding: utf-8 -*-

import json
import os
import re
from data_errors import DataValueError


def extract_digits(anystr):
    """Pull all digits from string in order and return"""
    return "".join(re.findall(ur'\d', anystr))


def validate_color(color):
    """Validate color field"""
    validator = ur'^[a-z ]+$'
    if re.match(validator, color):
        return color


def validate_name(name):
    """Validate name field"""
    validator = ur'^[A-Za-z .-]+$'
    if re.match(validator, name):
        return name


# Currently: any five digits
# Look into validation via db
# ftp://ftp2.census.gov/geo/tiger/TIGER2010/ZCTA5/2010/
def validate_zipcode(number):
    """Validate 5-digit U.S. Zipcode"""
    validator = ur'^\d{5}$'
    if re.match(validator, number):
        return number


def validate_zipcode_or_raise(zipcode):
    """Raise DataValueError if zipcode not valid"""
    code = validate_zipcode(zipcode)
    if not code:
        raise DataValueError('Bad5DigitZipcode', str(zipcode))
    return code

# validation expression adapted from expression and rules here:
# https://www.safaribooksonline.com/library/view/regular-expressions-cookbook/9781449327453/ch04s02.html
# could also try https://github.com/daviddrysdale/python-phonenumbers


# def validate_phonenumber(number):
#     """Validate 10-digit North American phone number"""
#     validator = ur'^[2-9][0-8][0-9][2-9][0-9]{6}$'
#     match = re.match(validator, number)
#     if match:
#         return number


# def validate_phonenumber_or_raise(number):
#     """Raise DataValueError if number not valid"""
#     digits = extract_digits(number)
#     if len(digits) == 11 and digits.startswith('1'):
#         digits = digits[1:]
#     number = validate_phonenumber(digits)
#     if not number:
#         raise DataValueError('BadPhoneNumber', str(digits))
#     return number


def validate_phonenumber(number):
    """Validate 10-digit North American phone number"""
    validator = ur'^\d{10}$'
    match = re.match(validator, number)
    if match:
        return number


def validate_phonenumber_or_raise(number):
    """Raise DataValueError if number not valid"""
    digits = extract_digits(number)
    number = validate_phonenumber(digits)
    if not number:
        raise DataValueError('BadPhoneNumber', str(digits))
    return '%s-%s-%s' % (number[0:3], number[3:6], number[6:10])


def validate_mi_or_raise(mi):
    """Raise DataValueError if m.i. not valid"""
    validator = ur'^[A-Z]\.$'
    if re.match(validator, mi):
        return mi
    else:
        raise DataValueError('BadMiddleInitialError', mi)


def preprocess_line(line):
    """Strip newline; split on comma; strip each resulting element"""
    elements = [element.strip() for element in line.strip("\n").split(',')]
    return elements


def write_json(json_obj, filename, sort_keys=True, indent=2):
    """Write formatted json to filename"""
    abspath = os.path.abspath(filename) # AttributeError
    with open(abspath, 'wb') as outfile: # IOError
        outfile.write(json.dumps(json_obj, sort_keys=sort_keys, indent=indent))
