#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Stealth Strings, hidden and dangerous."""


import base64
import binascii
import codecs
import zlib


def string2stealth(stringy: str, rot13: bool=False) -> str:
    """String to Stealth,stealth is a hidden string,both str type and utf-8."""
    stringy = codecs.encode(stringy, "rot-13") if rot13 and codecs else stringy
    strng = base64.b64encode(zlib.compress(stringy.strip().encode('utf-8'), 9))
    bits = bin(int(binascii.hexlify(strng), 16))[2:]
    return str(bits.zfill(8 * ((len(bits) + 7) // 8))).replace(
        "0", u"\u200B").replace("1", u"\uFEFF")
