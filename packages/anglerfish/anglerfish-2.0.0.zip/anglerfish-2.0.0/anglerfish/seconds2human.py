#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Calculate time, with precision from seconds to days."""


def seconds2human(time_on_seconds=0, do_year=True,
                  unit_words={"y": " Years ", "d": " Days ", "h": " Hours ",
                              "m": " Minutes ", "s": " Seconds "}):
    """Calculate time, with precision from seconds to days."""
    minutes, seconds = divmod(int(abs(time_on_seconds)), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    human_time_string = ""
    yea = "{0}" + str(unit_words.get("y", " Years "))
    dayz = "%02d" + str(unit_words.get("d", " Days "))
    hou = "%02d" + str(unit_words.get("h", " Hours "))
    minu = "%02d" + str(unit_words.get("m", " Minutes "))
    seco = "%02d" + str(unit_words.get("s", " Seconds "))
    years = int(int(days) / 365)
    if days and years and do_year and years > 1:
            human_time_string += yea.format(years)
            days = days - (365 * years)
    if days:
        human_time_string += dayz % days
    if hours:
        human_time_string += hou % hours
    if minutes:
        human_time_string += minu % minutes
    human_time_string += seco % seconds
    return human_time_string.strip()


def timedelta2human(time_delta, do_year=True,  # Just a shortcut :)
                    unit_words={"y": " Years ", "d": " Days ", "h": " Hours ",
                                "m": " Minutes ", "s": " Seconds "}):
    """Convert a TimeDelta object to human string representation."""
    return seconds2human(time_delta.total_seconds(),
                         do_year=do_year, unit_words=unit_words)
