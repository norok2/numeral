#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Numeral: integer-to-numeral conversion.
"""

# ======================================================================
# :: Future Imports
from __future__ import (
    division, absolute_import, print_function, unicode_literals)

# ======================================================================
# :: Python Standard Library Imports
import collections  # Container datatypes
import string  # Common string operations
import functools  # Higher-order functions and operations on callable objects
import math  # Mathematical functions
import doctest  # Test interactive Python examples

# ======================================================================
# :: Version
__version__ = '0.0.0.0'

# ======================================================================
# :: Project Details
INFO = {
    'author': 'Riccardo Metere <metere@cbs.mpg.de>',
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
_ROMAN_UNICODE_UPPER = collections.OrderedDict((
    ('Ⅰ', 1), ('Ⅱ', 2), ('Ⅲ', 3), ('Ⅳ', 4), ('Ⅴ', 5), ('Ⅵ', 6),
    ('Ⅶ', 7), ('Ⅷ', 8), ('Ⅸ', 9), ('Ⅹ', 10), ('Ⅺ', 11), ('Ⅻ', 12),
    ('Ⅼ', 50), ('Ⅽ', 100), ('Ⅾ', 500), ('Ⅿ', 1000), ('Ↄ', None), ('N', 0)))
_ROMAN_UNICODE_LOWER = collections.OrderedDict((
    ('ⅰ', 1), ('ⅱ', 2), ('ⅲ', 3), ('ⅳ', 4), ('ⅴ', 5), ('ⅵ', 6),
    ('ⅶ', 7), ('ⅷ', 8), ('ⅸ', 9), ('ⅹ', 10), ('ⅺ', 11), ('ⅻ', 12),
    ('ⅼ', 50), ('ⅽ', 100), ('ⅾ', 500), ('ⅿ', 1000), ('ↄ', None), ('n', 0)))
_ROMAN_UNICODE = _ROMAN_UNICODE_UPPER
_ROMAN_APOSTROPHUS = collections.OrderedDict((
    ('ↀ', 1000), ('ↁ', 5000), ('ↂ', 10000), ('ↇ', 50000), ('ↈ', 100000)))
_ROMAN_ARCHAIC = (('Ⅵ', 'ↅ'), ('Ⅼ', 'ↆ'))
_ROMAN_UNICODE_R = collections.OrderedDict(
    [(v, k) for k, v in sorted(_ROMAN_UNICODE.items(), reverse=True)
     if v is not None])
_ROMAN_APOSTROPHUS_R = collections.OrderedDict(
    [(v, k) for k, v in sorted(_ROMAN_APOSTROPHUS.items(), reverse=True)])
_ROMAN_UNICODE_TO_ASCII = (
    ('Ⅰ', 'I'), ('Ⅱ', 'II'), ('Ⅲ', 'III'), ('Ⅳ', 'IV'), ('Ⅴ', 'V'),
    ('Ⅵ', 'VI'), ('Ⅶ', 'VII'), ('Ⅷ', 'VIII'), ('Ⅸ', 'IX'), ('Ⅹ', 'X'),
    ('Ⅺ', 'XI'), ('Ⅻ', 'XII'), ('Ⅼ', 'L'), ('Ⅽ', 'C'), ('Ⅾ', 'D'),
    ('Ⅿ', 'M'), ('ↅ', 'VI'), ('ↀ', 'CD'), ('ↆ', 'L'), ('Ↄ', 'O'),
    ('ↁ', 'DO'), ('ↂ', 'CCDO'), ('ↇ', 'DOO'), ('ↈ', 'CCCDOO'))
_ROMAN_ASCII_UPPER = (
    ('I', 1), ('V', 5), ('X', 10), ('L', 50),
    ('C', 100), ('D', 500), ('M', 1000), ('N', 0))
_ROMAN_ASCII_LOWER = (
    ('i', 1), ('v', 5), ('x', 10), ('l', 50),
    ('c', 100), ('d', 500), ('m', 1000), ('n', 0))
_ROMAN_ASCII = _ROMAN_ASCII_UPPER


# ======================================================================
def _roman_max_consecutive(only_additive):
    return 4 if only_additive else 3


# ======================================================================
def multi_replace(
        text,
        replaces):
    """
    Perform multiple replacements in a string.

    Args:
        text (str): The input string.
        replaces (tuple[str,str]): The listing of the replacements.
            Format: ((<old>, <new>), ...).

    Returns:
        text (str): The string after the performed replacements.

    Examples:
        >>> multi_replace('python.best', (('thon', 'mrt'), ('est', 'ase')))
        'pymrt.base'
        >>> multi_replace('x-x-x-x', (('x', 'est'), ('est', 'test')))
        'test-test-test-test'
        >>> multi_replace('x-x-', (('-x-', '.test'),))
        'x.test'
    """
    return functools.reduce(lambda s, r: s.replace(*r), replaces, text)


# ======================================================================
def int2roman(
        num,
        only_ascii=False,
        only_additive=False,
        extended=True,
        uppercase=True,
        claudian=True,
        archaic=False,
        signed=True):
    """

    Args:
        num ():
        only_ascii (bool):
        only_additive (bool):
        extended (bool):
        uppercase (bool):
        claudian (bool):
        archaic (bool):
        signed (bool):

    Returns:

    Examples:
        >>> [int2roman(i) for i in range(13)]
        ['N', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ', 'Ⅹ', 'Ⅺ', 'Ⅻ']
        >>> [int2roman(i) for i in range(13, 23)]
        ['ⅩⅢ', 'ⅩⅣ', 'ⅩⅤ', 'ⅩⅥ', 'ⅩⅦ', 'ⅩⅧ', 'ⅩⅨ', 'ⅩⅩ', 'ⅩⅪ', 'ⅩⅫ']
        >>> [int2roman(i) for i in [44, 51, 62, 73, 84, 95, 99]]
        ['ⅩⅬⅣ', 'ⅬⅠ', 'ⅬⅫ', 'ⅬⅩⅩⅢ', 'ⅬⅩⅩⅩⅣ', 'ⅬⅩⅬⅤ', 'ⅬⅩⅬⅨ']
        >>> [int2roman(i) for i in range(1666, 3999, 517)]
        ['ⅯⅮⅭⅬⅩⅥ', 'ⅯⅯⅭⅬⅩⅩⅩⅢ', 'ⅯⅯⅮⅭⅭ', 'ⅯⅯⅯⅭⅭⅩⅦ', 'ⅯⅯⅯⅮⅭⅭⅩⅩⅩⅣ']
        >>> [int2roman(2 ** i) for i in range(14, 17)]
        ['ⅭↀↃⅮↃⅯⅭⅭⅭⅬⅩⅩⅩⅣ', 'ⅭↀↃⅭↀↃⅭↀↃⅯⅯⅮⅭⅭⅬⅩⅧ', 'ⅮↃↃⅭↀↃⅮↃⅮⅩⅩⅩⅥ']
        >>> [int2roman(i) for i in [4000, 40000, 5000, 10000, 50000, 100000]]
        ['MⅮↃ', 'ⅭↀↃⅮↃↃ', 'ⅮↃ', 'ⅭↀↃ', 'ⅮↃↃ', 'ⅭⅭↀↃↃ']
        >>> [int2roman(i, archaic=True) for i in [26, 27, 55, 56, 59]]
        ['ⅩⅩↅ', 'ⅩⅩⅦ', 'ↆⅤ', 'ↆↅ', 'ↆⅨ']
        >>> [int2roman(i, only_ascii=True) for i in [1666, 3999, 4000, 16384]]
        ['MDCLXVI', 'MMMDCDLXLIX', 'MDO', 'CCDODOMCCCLXXXIV']

    """
    text = ''
    # update max_consecutive
    max_consecutive = _roman_max_consecutive(only_additive)
    # handles negative numbers
    if num < 0:
        if signed:
            text += '-'
            num = abs(num)
        else:
            raise ValueError('`{}` needs `signed` option'.format(num))
    # handles the zero
    if num == 0:
        if extended:
            text = _ROMAN_UNICODE_R[0]
        else:
            raise ValueError('`{}` needs `extended` option'.format(num))
    else:  # handles positive integers
        last_key, prev_key = None, None
        consecutive = 0
        max_standard = max(_ROMAN_UNICODE_R.keys())
        while num > 0:
            if num < max_standard * (max_consecutive + 1):
                for val, key in _ROMAN_UNICODE_R.items():
                    if val and num - val >= 0 and val not in (11, 12):
                        if key == last_key:
                            consecutive += 1
                        else:
                            consecutive = 0
                        if 0 <= consecutive < max_consecutive:
                            text += key
                            num -= val
                            last_key = key
                            break
                        else:
                            text = text[:-max_consecutive + 1] + prev_key
                            num -= val
                            break
                    prev_key = key if val not in (11, 12) else prev_key
            elif extended:
                max_apostrophus = max(_ROMAN_APOSTROPHUS_R.values())
                log_m = math.log10(_ROMAN_APOSTROPHUS['ↀ'])
                log_num = math.log10(num)
                is_half = num >= 5 * 10 ** int(log_num)
                repeat = int(log_num) - int(log_m) + (1 if is_half else 0)
                tmp_num = (5 if is_half else 1) * 10 ** int(log_num)
                correction = -2 * tmp_num \
                    if num >= tmp_num * (max_consecutive + 1) else 0
                if claudian:
                    prefix = 'Ⅾ' if is_half else (
                        'Ⅽ' * repeat + ('ↀ' if repeat else 'M'))
                    text += prefix + 'Ↄ' * repeat
                elif num < max_apostrophus * (max_consecutive + 1):
                    text += _ROMAN_APOSTROPHUS[tmp_num]
                else:
                    raise ValueError(
                        '`{}` needs `claudian` option'.format(num))
                num -= tmp_num + correction
            else:
                raise ValueError('`{}` needs `extended` option'.format(num))
    text = multi_replace(text, (('ⅩⅠ', 'Ⅺ'), ('ⅩⅡ', 'Ⅻ')))
    if archaic:
        text = multi_replace(text, _ROMAN_ARCHAIC)
    if only_ascii:
        text = multi_replace(text, _ROMAN_UNICODE_TO_ASCII)
    text = text.upper() if uppercase else text.lower()
    return text


# ======================================================================
def roman2int(text):
    """

    Args:
        text ():

    Returns:


    Examples:
        >>> roman2int('MDCLXVI')
        1666
    """
    num = None
    text = text.strip().upper()
    text = multi_replace(text, _ROMAN_UNICODE_TO_ASCII)
    text = multi_replace(text, tuple([(i, j) for (j, i) in _ROMAN_ARCHAIC]))
    valid_chars = True
    if valid_chars:
        pass
    else:
        raise ValueError('Input contains invalid characters')
    return num


# ======================================================================
def int2letter(
        num,
        alphabet=string.ascii_lowercase):
    """

    Args:
        num ():
        alphabet ():

    Returns:

    Examples:
        >>> [int2letter(i) for i in range(14)]
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
        >>> int2letter(23)
        'x'
        >>> int2letter(26)
        'aa'
        >>> int2letter(702)
        'aaa'
        >>> int2letter(1983)
        'bxh'
        >>> for n in range(100):
        ...     assert(n == letter2int(int2letter(n)))
    """
    return int2tokens(num, alphabet)


# ======================================================================
def letter2int(
        text,
        alphabet=string.ascii_lowercase):
    """

    Args:
        text ():
        alphabet ():

    Returns:

    Examples:
        >>> [letter2int(s) for s in ['a', 'z', 'aa', 'aaa', 'aab', 'bxh']]
        [0, 25, 26, 702, 703, 1983]
        >>> for n in range(100, 200):
        ...     assert(n == letter2int(int2letter(n)))
    """
    num = 0
    for i, letter in enumerate(text[::-1]):
        offset = 0 if i == 0 else 1
        num += (alphabet.index(letter) + offset) * len(alphabet) ** i
    return num


# ======================================================================
def int2tokens(
        num,
        tokens):
    """

    Args:
        num ():
        tokens ():

    Returns:

    Examples:
        >>> [int2tokens(i, ('0', '1')) for i in range(10)]
        ['0', '1', '00', '01', '10', '11', '000', '001', '010', '011']
        >>> [int2tokens(i, ('a', 'b', 'c')) for i in range(10)]
        ['a', 'b', 'c', 'aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca']
        >>> [int2tokens(i, 'abc') for i in range(10)]
        ['a', 'b', 'c', 'aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca']
        >>> [int2tokens(i, ('po', 'ta')) for i in range(8)]
        ['po', 'ta', 'popo', 'pota', 'tapo', 'tata', 'popopo', 'popota']
        >>> int2tokens(161, ('po', 'ta'))
        'potapopopotata'
        >>> d = ('mo', 'no', 'ke')
        >>> for n in range(100):
        ...     assert(n == tokens2int(int2tokens(n, d), d))
    """
    text = ''
    while num >= 0:
        text = tokens[num % len(tokens)] + text
        num = num // len(tokens) - 1
    return text


# ======================================================================
def tokens2int(
        text,
        tokens):
    """

    Args:
        text ():
        tokens ():

    Returns:

    Examples:
        >>> [tokens2int(s, ('po', 'ta')) for s in ['po', 'ta', 'popo', 'pota']]
        [0, 1, 2, 3]
        >>> tokens2int('potapopopotata', ('po', 'ta'))
        161
        >>> d = ('mo', 'no', 'ke')
        >>> for n in range(100, 200):
        ...     assert(n == tokens2int(int2tokens(n, d), d))
    """
    num = 0
    i = 0
    found = True
    while text or not found:
        found = False
        for j, token in enumerate(tokens):
            if text.endswith(token):
                text = text[:-len(token)]
                offset = 0 if i == 0 else 1
                num += (j + offset) * len(tokens) ** i
                found = True
                i += 1
    return num


# ======================================================================
def main():
    print(__doc__.strip())
    doctest.testmod()


# ======================================================================
if __name__ == '__main__':
    main()
