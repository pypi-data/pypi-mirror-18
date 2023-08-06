#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Common exceptions for anglerfish."""


class AnglerfishException(Exception):
    """Common exceptions for anglerfish."""
    pass


class NamespaceConflictError(ImportError, AnglerfishException):
    """Common exceptions for anglerfish."""
    pass
