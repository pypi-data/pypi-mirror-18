#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Get current public IP as string."""


from urllib.request import urlopen


def get_public_ip():
    """Get current public IP as string."""
    return urlopen("https://api.ipify.org").read().decode("utf-8").strip()


def is_online():
    """Check if we got internet conectivity."""
    try:
        get_public_ip()
    except:
        return False
    else:
        return True
