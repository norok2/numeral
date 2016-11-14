#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DESCRIPTION OF THE FILE CONTENT IS MISSING!
"""

# ======================================================================
# :: Future Imports
from __future__ import (
    division, absolute_import, print_function, unicode_literals)

# ======================================================================
# :: Python Standard Library Imports
# import os  # Miscellaneous operating system interfaces
# import sys  # System-specific parameters and functions
# import shutil  # High-level file operations
# import platform  # Access to underlying platform’s identifying data
# import math  # Mathematical functions
# import time  # Time access and conversions
# import datetime  # Basic date and time types
# import re  # Regular expression operations
# import operator  # Standard operators as functions
# import collections  # High-performance container datatypes
import argparse  # Parser for command-line options, arguments and subcommands

# ======================================================================
# :: Version
__version__ = '0.0.0.1'

# ======================================================================
# :: Project Details
INFO = {
    'authors': (
        'Riccardo Metere <rick@metere.it>',
    ),
    'copyright': 'Copyright (C) 2016',
    'license': 'GNU General Public License version 3 or later (GPLv3+)',
    'notice':
        """
This program is free software and it comes with ABSOLUTELY NO WARRANTY.
It is covered by the GNU General Public License version 3 (GPLv3).
You are welcome to redistribute it under its terms and conditions.
        """,
    'version': __version__
}

# ======================================================================
# :: supported verbosity levels
VERB_LVL_NAMES = (
    'none', 'lowest', 'lower', 'low', 'medium', 'high', 'higher', 'highest',
    'warning', 'debug')
VERB_LVL = {k: v for k, v in zip(VERB_LVL_NAMES, range(len(VERB_LVL_NAMES)))}
D_VERB_LVL = VERB_LVL['lowest']

# ======================================================================
# Greetings
MY_GREETINGS = r"""
 ____        ____ ___
|  _ \ _   _|  _ \_ _|
| |_) | | | | |_) | |
|  __/| |_| |  __/| |
|_|    \__, |_|  |___|
       |___/
"""
# generated with: figlet 'PyMRT' -f standard

# :: Causes the greetings to be printed any time the library is loaded.
print(MY_GREETINGS)


# ======================================================================
def msg(
        text,
        verb_lvl=D_VERB_LVL,
        verb_threshold=D_VERB_LVL,
        fmt=None,
        *args,
        **kwargs):
    """
    Display a feedback message to the standard output.

    Args:
        text (str|Any): Message to display or object with `__repr__`.
        verb_lvl (int): Current level of verbosity.
        verb_threshold (int): Threshold level of verbosity.
        fmt (str): Format of the message (if `blessed` supported).
            If None, a standard formatting is used.
        *args (tuple): Positional arguments to be passed to `print`.
        **kwargs (dict): Keyword arguments to be passed to `print`.

    Returns:
        None.

    Examples:
        >>> s = 'Hello World!'
        >>> msg(s)
        Hello World!
        >>> msg(s, VERB_LVL['medium'], VERB_LVL['low'])
        Hello World!
        >>> msg(s, VERB_LVL['low'], VERB_LVL['medium'])  # no output
        >>> msg(s, fmt='{t.green}')  # if ANSI Terminal, green text
        Hello World!
        >>> msg('   :  a b c', fmt='{t.red}{}')  # if ANSI Terminal, red text
           :  a b c
        >>> msg(' : a b c', fmt='cyan')  # if ANSI Terminal, cyan text
         : a b c
    """
    if verb_lvl >= verb_threshold and text:
        # if blessed is not present, no coloring
        try:
            import blessed
        except ImportError:
            blessed = None

        text = str(text)

        if blessed:
            t = blessed.Terminal()
            if not fmt:
                if VERB_LVL['low'] < verb_threshold <= VERB_LVL['medium']:
                    e = t.cyan
                elif VERB_LVL['medium'] < verb_threshold < VERB_LVL['debug']:
                    e = t.magenta
                elif verb_threshold >= VERB_LVL['debug']:
                    e = t.blue
                elif text.startswith('I:'):
                    e = t.green
                elif text.startswith('W:'):
                    e = t.yellow
                elif text.startswith('E:'):
                    e = t.red
                else:
                    e = t.white
                # first non-whitespace word
                txt1 = text.split(None, 1)[0]
                # initial whitespaces
                n = text.find(txt1)
                txt0 = text[:n]
                # rest
                txt2 = text[n + len(txt1):]
                txt_kwargs = {
                    'e1': e + (t.bold if e == t.white else ''),
                    'e2': e + (t.bold if e != t.white else ''),
                    't0': txt0, 't1': txt1, 't2': txt2, 'n': t.normal}
                text = '{t0}{e1}{t1}{n}{e2}{t2}{n}'.format_map(txt_kwargs)
            else:
                if 't.' not in fmt:
                    fmt = '{{t.{}}}'.format(fmt)
                if '{}' not in fmt:
                    fmt += '{}'
                text = fmt.format(text, t=t) + t.normal
        print(text, *args, **kwargs)


# ======================================================================
def distribute():
    pass


# ======================================================================
def handle_arg():
    """
    Handle command-line application arguments.
    """
    # :: Create Argument Parser
    arg_parser = argparse.ArgumentParser(
        description=__doc__,
        epilog='v.{} - {}\n{}'.format(
            INFO['version'], ', '.join(INFO['authors']), INFO['license']),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # :: Add POSIX standard arguments
    arg_parser.add_argument(
        '--ver', '--version',
        version='%(prog)s - ver. {}\n{}\n{} {}\n{}'.format(
            INFO['version'],
            next(line for line in __doc__.splitlines() if line),
            INFO['copyright'], ', '.join(INFO['authors']),
            INFO['notice']),
        action='version')
    arg_parser.add_argument(
        '-v', '--verbose',
        action='count', default=D_VERB_LVL,
        help='increase the level of verbosity [%(default)s]')
    arg_parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='override verbosity settings to suppress output [%(default)s]')
    # :: Add additional arguments
    arg_parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='force new processing [%(default)s]')
    return arg_parser


# ======================================================================
def main():
    # :: handle program parameters
    arg_parser = handle_arg()
    args = arg_parser.parse_args()
    # fix verbosity in case of 'quiet'
    if args.quiet:
        args.verbose = VERB_LVL['none']
    # :: print debug info
    if args.verbose >= VERB_LVL['debug']:
        arg_parser.print_help()
        msg('\nARGS: ' + str(vars(args)), args.verbose, VERB_LVL['debug'])
    msg(__doc__.strip())

    # run code here


# ======================================================================
if __name__ == '__main__':
    main()
