#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Format number as currency money with thousand separator, 2 decimals."""


def number2currency(value, decimals=2, sign="$"):
    """Format number as currency money with thousand separator, 2 decimals."""
    number, decimal = (('%%,%df' % decimals) % value).split(',')
    parts = []
    while len(number) > 3:
        part, number = number[-3:], number[:-3]
        parts.append(part)
    parts.append(number)
    parts.reverse()
    if int(decimal) == 0:
        currency_money = '.'.join(parts) + sign
    else:
        currency_money = '.'.join(parts) + ',' + decimal + sign
    return currency_money
