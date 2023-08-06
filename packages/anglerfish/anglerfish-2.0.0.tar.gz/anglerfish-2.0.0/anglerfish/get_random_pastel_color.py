#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Get a random pastel color as string, useful for HTML/CSS styling."""


# This 2 groups have been tested on HTML/CSS with one each other,
# they look pretty good on all combinations, we are not Designers,
# but this is useful for quick templating and boilerplates styling.


from random import choice


def get_random_pastelight_color():
    """Get a random pastel light color as string, useful for CSS styling."""
    return choice((
        'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige',
        'cornsilk', 'floralwhite', 'ghostwhite', 'grey',
        'honeydew', 'ivory', 'lavender',
        'lavenderblush', 'lemonchiffon', 'lightcyan',
        'lightgoldenrodyellow', 'lightgrey', 'lightpink', 'lightskyblue',
        'lightyellow', 'linen', 'mint', 'mintcream', 'oldlace', 'papayawhip',
        'peachpuff', 'seashell', 'skyblue', 'snow', 'thistle', 'white'))


def get_random_pasteldark_color():
    """Get a random dark color as string, useful for CSS styling."""
    return choice((
        'brown', 'chocolate', 'crimson', 'darkblue', 'darkgoldenrod',
        'darkgray', 'darkgreen', 'darkolivegreen', 'darkorange', 'darkred',
        'darkslateblue', 'darkslategray', 'dimgray', 'dodgerblue',
        'firebrick', 'forestgreen', 'indigo', 'maroon', 'mediumblue',
        'midnightblue', 'navy', 'olive', 'olivedrab', 'royalblue',
        'saddlebrown', 'seagreen', 'sienna', 'slategray', 'teal'))


def get_random_pastel_color():
    """Get a random dark or light color as string, useful for CSS styling."""
    return choice((get_random_pastelight_color(),
                   get_random_pasteldark_color()))
