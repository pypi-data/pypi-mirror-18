#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Set process I/O and cpu priority."""


import logging as log
import os

from shutil import which
from subprocess import call


def set_process_priority(nice=True, ionice=False):
    """Set process name and cpu priority."""
    w = "IONice may delay I/O Operations, not recommended on user-facing GUI!."
    try:
        if nice:
            old = os.getpriority(os.PRIO_PROCESS, 0)
            os.nice(19)  # smooth cpu priority
            log.debug("Process CPUs Priority set: from {0} to 19.".format(old))
        elif ionice and which("ionice"):
            log.warning(w)
            command = "{0} --ignore --class 3 --pid {1}".format(
                which("ionice"), os.getpid())
            call(command, shell=True)  # I/O nice,should work on Linux and Os X
            log.debug("Process I/O Priority set to: {0}.".format(command))
    except Exception as error:
        log.warning(error)
        return False  # this may fail on windows and its normal, so be silent.
    else:
        return True
