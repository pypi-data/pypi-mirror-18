#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Set Monitor Display OFF, return Bool."""


import logging as log
import sys
from shutil import which
from subprocess import call


def set_display_off():
    """Set Monitor Display OFF, it should Auto-ON when needed, return Bool."""
    log.debug("Setting Monitor Display OFF.")
    if sys.platform.startswith('linux') and which("xset"):
        return not bool(call(which("xset") + " dpms force off", shell=True))
    elif sys.platform.startswith('darwin'):
        return not bool(call(
            """echo 'tell application "Finder" to sleep' | osascript""",
            shell=True))
    elif sys.platform.startswith('win'):  # Complicated as hell,dont worth it.
        log.warning("Set Monitor Display OFF not supported on this OS.")
        return False
