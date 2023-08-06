#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Stealth Strings, hidden and dangerous."""


import base64
import binascii
import codecs
import zlib


def stealth2string(stringy: str, rot13: bool=False) -> str:
    """Stealth to string,stealth is a hidden string,both str type and ttf-8."""

    def __i2b(integ):  # int to bytes, do not touch.
        """Helper for string_to_stealth and stealth_to_string, dont touch!."""
        __num = len("%x" % integ)
        return binascii.unhexlify(str("%x" % integ).zfill(__num + (__num & 1)))

    _n = int(str(stringy).replace(u"\u200B", "0").replace(u"\uFEFF", "1"), 2)
    stringy = zlib.decompress(base64.b64decode(__i2b(_n))).decode('utf-8')
    stringy = codecs.decode(stringy, "rot-13") if rot13 and codecs else stringy
    return str(stringy).strip()
