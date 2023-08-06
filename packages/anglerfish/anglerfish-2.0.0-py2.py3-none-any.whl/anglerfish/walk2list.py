#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Perform full walk of where, gather full path of all files."""


import logging as log
import os

from typing import NamedTuple


def walk2list(where, target, omit, links=False, tuply=True, namedtuple=None):
    """Perform full walk of where, gather full path of all files."""
    log.debug("Scan {},searching {},ignoring {},{}following SymLinks.".format(
        where, target, omit, "" if links else "Not "))
    listy = [os.path.abspath(os.path.join(r, f))
             for r, d, fs in os.walk(where, followlinks=links)
             for f in fs if not f.startswith('.') and
             not f.endswith(omit) and
             f.endswith(target)]  # only target files,no hidden files
    list_of_files = listy
    if tuply:  # Return a Tuple.
        list_of_files = tuple(listy)
    if namedtuple:  # Return a NamedTuple with static typing.
        namedtuple_of_files = NamedTuple(  # You can work comfortably using
            str(namedtuple).strip(),  # myfolder.path_9 instead of myfolder[9]
            fields=(("path_{0}".format(i), str) for i in range(len(listy))))
        list_of_files = namedtuple_of_files(*listy)
    return list_of_files
