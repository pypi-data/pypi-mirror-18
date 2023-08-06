#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Set process name and cpu priority."""


import logging as log

from ctypes import byref, cdll, create_string_buffer


def set_process_name(name):
    """Set process name and cpu priority."""
    name = str(name).lower().strip()
    try:
        libc = cdll.LoadLibrary("libc.so.6")  # set process name
        buff = create_string_buffer(len(name) + 1)
        buff.value = bytes(name.encode("utf-8"))
        libc.prctl(15, byref(buff), 0, 0, 0)
    except Exception as error:
        log.warning(error)
        return False  # this may fail on windows and its normal, so be silent.
    else:
        log.debug("Process Name set to: {0}.".format(name))
        return True
