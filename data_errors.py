# -*- coding: utf-8 -*-

import logging
import traceback


class DataValueError(ValueError):
    def __init__(self, err_type, value):
        ValueError.__init__(self)
        self.err_type = err_type
        self.value = value

    def __str__(self):
        return repr(self.err_type+"\t"+self.value)



def data_excepthook(err_type, value, tb):
    logging.error(
        "".join(traceback.format_exception(err_type, value, tb))
    )

