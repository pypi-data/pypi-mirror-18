#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Import a module from file path string."""


import errno
import importlib.util
import logging as log
import os

from .exceptions import NamespaceConflictError


def path2import(pat, name=None, ignore_exceptions=False, check_namespace=True):
    """Import a module from file path string.

    This is "as best as it can be" way to load a module from a file path string
    that I can find from the official Python Docs, for Python 3.5+.
    """
    module = None
    if not os.path.isfile(pat):
        if not ignore_exceptions:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), pat)
    elif not os.access(pat, os.R_OK):
        if not ignore_exceptions:
            raise PermissionError(pat)
    else:
        try:
            name = name or os.path.splitext(os.path.basename(pat))[0]
            if check_namespace and name in globals():
                e = "Module {0} already exist on global namespace".format(name)
                if not ignore_exceptions:
                    raise NamespaceConflictError(e)
            else:
                spec = importlib.util.spec_from_file_location(name, pat)
                if spec is None:
                    e = 'Failed to load module {0} from {1}.'.format(name, pat)
                    if not ignore_exceptions:
                        raise ImportError(e)
                module = spec.loader.load_module()
        except Exception as error:
            log.warning("Failed to Load Module {0} from {1}".format(name, pat))
            log.warning(error)
            if not ignore_exceptions:
                raise
            module = None
        else:
            log.debug("Loading Module {0} from path {1}.".format(name, pat))
    return module
