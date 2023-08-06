#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Multithreading helper."""


from concurrent.futures import ThreadPoolExecutor
from functools import wraps


class _Threaded():

    """Basic Threaded class."""

    def __init__(self, future, timeout):
        """Init _Threaded class, set class attributes."""
        self._future, self._timeout = future, timeout

    def __getattr__(self, name):
        """Get and return the name attribute."""
        result = self._wait()
        return result.__getattribute__(name)

    def _wait(self):
        """Get wait."""
        return self._future.result(self._timeout)


def _async(n, base_type, timeout=None):
    """Async internal function for decorator."""
    def decorator(f):
        """Decorator builder."""
        if isinstance(n, int):
            pool = base_type(n)
        elif isinstance(n, base_type):
            pool = n
        else:
            raise TypeError("Invalid Type: {}".format(type(base_type)))

        @wraps(f)
        def wrapped(*args, **kwargs):
            """Return the wrapped function."""
            return _Threaded(pool.submit(f, *args, **kwargs), timeout=timeout)
        return wrapped

    return decorator


def threads(n, timeout=None):
    """Convert a simple function to multrithreading."""
    return _async(n, ThreadPoolExecutor, timeout)
