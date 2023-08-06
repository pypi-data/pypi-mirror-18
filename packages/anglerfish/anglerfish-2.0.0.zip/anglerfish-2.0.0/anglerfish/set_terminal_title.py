#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Set or Reset CLI Window Titlebar Title."""


import os
import sys
from shutil import which


def set_terminal_title(titlez=""):
    """Set or Reset CLI Window Titlebar Title."""
    if titlez and isinstance(titlez, str) and len(titlez.strip()):
        if sys.platform.startswith('win'):  # Windows:
            os.system(which("title") + " {0}".format(titlez.strip()))
        else:  # Linux, Os X and otherwise
            print(r"\x1B]0; {0} \x07".format(titlez.strip()))
        return titlez
    else:
        if sys.platform.startswith('win'):
            os.system(which("title"))
        else:
            print(r"\x1B]0;\x07")
        return ""  # Title should be "" so we return ""
