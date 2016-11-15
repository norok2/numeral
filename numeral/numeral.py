#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Numeral: support for various integer-to-numeral (and back) conversion.
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
import re  # Regular expression operations
import doctest  # Test interactive Python examples

# ======================================================================
# :: Version
try:
    from numeral._version import __version__
except ImportError:
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
    ('Ⅼ', 50), ('Ⅽ', 100), ('Ⅾ', 500), ('Ⅿ', 1000), ('N', 0), ('Ↄ', None)))
_ROMAN_UNICODE_LOWER = collections.OrderedDict((
    ('ⅰ', 1), ('ⅱ', 2), ('ⅲ', 3), ('ⅳ', 4), ('ⅴ', 5), ('ⅵ', 6),
    ('ⅶ', 7), ('ⅷ', 8), ('ⅸ', 9), ('ⅹ', 10), ('ⅺ', 11), ('ⅻ', 12),
    ('ⅼ', 50), ('ⅽ', 100), ('ⅾ', 500), ('ⅿ', 1000), ('n', 0), ('ↄ', None)))
_ROMAN_UNICODE = _ROMAN_UNICODE_UPPER
_ROMAN_UNICODE_R = collections.OrderedDict(
    [(v, k) for k, v in sorted(_ROMAN_UNICODE.items(), reverse=True)
     if v is not None])
_ROMAN_APOSTROPHUS = collections.OrderedDict((
    ('ↀ', 1000), ('ↁ', 5000), ('ↂ', 10000), ('ↇ', 50000), ('ↈ', 100000)))
_ROMAN_APOSTROPHUS_R = collections.OrderedDict(
    [(v, k) for k, v in sorted(_ROMAN_APOSTROPHUS.items(), reverse=True)])
_ROMAN_CLAUDIAN_TO_APOSTROPHUS = (
    ('ⅭⅭↀↃↃ', 'ↈ'), ('ⅮↃↃ', 'ↇ'), ('ⅭↀↃ', 'ↂ'), ('ⅮↃ', 'ↁ'))
_ROMAN_CLAUDIAN_TO_APOSTROPHUS_R = tuple(
    [(v, k) for k, v in _ROMAN_CLAUDIAN_TO_APOSTROPHUS])
_ROMAN_CLAUDIAN_TO_ASCII = 'O'  # arbitrarily chosen ASCII equivalent of `Ↄ`
_ROMAN_UNICODE_TO_ASCII = (
    ('Ⅰ', 'I'), ('Ⅱ', 'II'), ('Ⅲ', 'III'), ('Ⅳ', 'IV'), ('Ⅴ', 'V'),
    ('Ⅵ', 'VI'), ('Ⅶ', 'VII'), ('Ⅷ', 'VIII'), ('Ⅸ', 'IX'), ('Ⅹ', 'X'),
    ('Ⅺ', 'XI'), ('Ⅻ', 'XII'), ('Ⅼ', 'L'), ('Ⅽ', 'C'), ('Ⅾ', 'D'),
    ('Ⅿ', 'M'), ('ↅ', 'VI'), ('ↀ', 'CD'), ('ↆ', 'L'), ('N', 'N'),
    ('Ↄ', _ROMAN_CLAUDIAN_TO_ASCII),
    ('ↁ', 'D' + _ROMAN_CLAUDIAN_TO_ASCII),
    ('ↂ', 'CCD' + _ROMAN_CLAUDIAN_TO_ASCII),
    ('ↇ', 'D' + _ROMAN_CLAUDIAN_TO_ASCII * 2),
    ('ↈ', 'CCCD' + _ROMAN_CLAUDIAN_TO_ASCII * 2))
_ROMAN_ASCII_UPPER = collections.OrderedDict((
    ('I', 1), ('V', 5), ('X', 10), ('L', 50),
    ('C', 100), ('D', 500), ('M', 1000), ('N', 0),
    (_ROMAN_CLAUDIAN_TO_ASCII, None)))
_ROMAN_ASCII_LOWER = collections.OrderedDict((
    ('i', 1), ('v', 5), ('x', 10), ('l', 50),
    ('cⅽ', 100), ('d', 500), ('m', 1000), ('n', 0),
    (_ROMAN_CLAUDIAN_TO_ASCII.lower(), None)))
_ROMAN_ASCII = _ROMAN_ASCII_UPPER
_ROMAN_ASCII_R = collections.OrderedDict(
    [(v, k) for k, v in sorted(_ROMAN_ASCII.items(), reverse=True)
     if v is not None])
_ROMAN_MINUS = '-'
_ROMAN_MAX_CONSECUTIVE = {True: 4, False: 3}  # key -> `only_additive` option
_ROMAN_STRICT_REGEX = \
    r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'

# ======================================================================
ROMAN_ALTERNATIVES = (('Ⅵ', 'ↅ'), ('Ⅼ', 'ↆ'), ('Ⅿ', 'ↀ'))


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
def int2letter(
        num,
        alphabet=string.ascii_lowercase,
        negative_sign='-'):
    """
    Convert a number to the least amount letters (within an alphabet).

    Items in the alphabet must not repeat.

    This is the inverse of `letter2int()` given the same alphabet.

    Args:
        num (int): The input number to convert.
        alphabet (str): The alphabet to use for the representation.
            Characters within the alphabet must not repeat.
        negative_sign (str): The symbol to use for negative numbers.
            The negative sign will be the first character of the representation.

    Returns:
        text (str): The integer represented.

    Examples:
        >>> [int2letter(i) for i in range(14)]
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
        >>> [int2letter(i) for i in [23, 26, 27, 28, 29, 702, 703, 704, 1983]]
        ['x', 'aa', 'ab', 'ac', 'ad', 'aaa', 'aab', 'aac', 'bxh']
        >>> all([n == letter2int(int2letter(n)) for n in range(-999, 99)])
        True

    See Also:
        letter2int(), tokens2int(), int2tokens()
    """
    return int2tokens(num, alphabet, negative_sign)


# ======================================================================
def letter2int(
        text,
        alphabet=string.ascii_lowercase,
        negative_sign='-'):
    """
    Convert a group of letters (within a given alphabet) to a number.

    Items in the alphabet must not repeat.

    This is the inverse of `int2letter()` given the same alphabet.

    Args:
        text (str): The input string to parse.
        alphabet (str): The alphabet to use for the representation.
            Characters within the alphabet must not repeat.
        negative_sign (str): The symbol to use for negative numbers.
            The negative sign must be the first character of the representation.

    Returns:
        num (int): The integer represented.

    Raises:
        ValueError: if text contains non-alphabet characters
        ValueError: if `negative_sign` is in `alphabet`
        ValueError: if `negative_sign` is present but not the first item

    Examples:
        >>> [letter2int(s) for s in ['a', 'z', 'aa', 'ad', 'aaa', 'aab', 'bxh']]
        [0, 25, 26, 29, 702, 703, 1983]
        >>> all([n == letter2int(int2letter(n)) for n in range(-99, 999)])
        True

    See Also:
        int2letter(), tokens2int(), int2tokens()
    """
    num = 0
    sign = 1
    text = text.strip()
    if negative_sign in alphabet:
        raise ValueError('Alphabet and negative sign must not overlap')
    if negative_sign in text:
        if text[0] == negative_sign:
            text = text[1:]
            sign = -1
        else:
            raise ValueError('Negative sign is in wrong position')
    if not set(text).issubset(set(alphabet)):
        raise ValueError('Text contains invalid characters')
    for i, letter in enumerate(text[::-1]):
        offset = 0 if i == 0 else 1
        num += (alphabet.index(letter) + offset) * len(alphabet) ** i
    return num * sign


# ======================================================================
def int2tokens(
        num,
        tokens,
        negative_sign='-'):
    """
    Convert a group of tokens (within a given set) to a number.

    Items in the tokens set must not repeat/overlap.

    This is the inverse of `int2tokens()` given the same tokens set.

    Args:
        num (int): The input number to convert.
        tokens (iterable[str]): The tokens to use for the representation.
            Items within the tokens set must not repeat or overlap.
        negative_sign (str): The symbol to use for negative numbers.
            The negative sign will be the first character of the representation.

    Returns:
        text (str): The integer represented.

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
        >>> all([n == tokens2int(int2tokens(n, d), d) for n in range(-999, 99)])
        True

    See Also:
        letter2int(), int2letter(), tokens2int()
    """
    text = ''
    if num < 0:
        sign_text = negative_sign
        num = abs(num)
    else:
        sign_text = ''
    while num >= 0:
        text = tokens[num % len(tokens)] + text
        num = num // len(tokens) - 1
    return sign_text + text


# ======================================================================
def tokens2int(
        text,
        tokens,
        negative_sign='-'):
    """
    Convert a number to the least amount tokens (within a tokens set).

    Items in the tokens set must not repeat/overlap.

    This is the inverse of `tokens2int()` given the same tokens set.

    Args:
        text (str): The input string to parse.
        tokens (iterable[str]): The tokens to use for the representation.
            Items within the tokens set must not repeat or overlap.
        negative_sign (str): The symbol to use for negative numbers.
            The negative sign must be the first character of the representation.

    Returns:
        num (int): The integer represented.

    Examples:
        >>> [tokens2int(s, ('po', 'ta')) for s in ['po', 'ta', 'popo', 'pota']]
        [0, 1, 2, 3]
        >>> tokens2int('potapopopotata', ('po', 'ta'))
        161
        >>> d = ('mo', 'no', 'ke')
        >>> all([n == tokens2int(int2tokens(n, d), d) for n in range(-99, 999)])
        True

    See Also:
        letter2int(), int2letter(), int2tokens()
    """
    num = 0
    sign = 1
    text = text.strip()
    if negative_sign in tokens:
        raise ValueError('Negative sign must not be a token')
    if negative_sign in text:
        if text[0] == negative_sign:
            text = text[1:]
            sign = -1
        else:
            raise ValueError('Negative sign is in wrong position')
    if not set(text).issubset(set(''.join(tokens))):
        raise ValueError('Text contains invalid characters')
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
    return num * sign


# ======================================================================
def int2roman(
        num,
        only_ascii=False,
        only_additive=False,
        extended=True,
        uppercase=True,
        claudian=False,
        alternatives=None,
        signed=True,
        negative_sign=_ROMAN_MINUS):
    """
    Convert an integer to its corresponding Roman number representation.

    Args:
        num (int): The input number to convert
        only_ascii (bool): Force the use of only-ASCII characters.
            If True only valid ASCII characters are used.
            The Apostrophus notation is forced to expand using the Claudian
            symbol (a specular C), which is in turn converted to a valid ASCII
            character with some resemblance to it, i.e. the letter `O`.
        only_additive (bool): Force only-additive notation.
            This means that the symbols are strictly sorted according decreasing
            value left-to-right and they all add up.
            Otherwise, a single lower-value symbol preceding a larger-value one
            is used to indicate subtraction, thus avoiding 4 symbols repetition.
        extended (bool): Allow for 0 and large numbers to be included.
            Large numbers are above 3999 if `only_additive` is False,
            otherwise they are above 4999.
        uppercase (bool): Use uppercase for the output.
            If False, the output is converted to lowercase.
        claudian (bool): Force the use of Claudian for apostrophus notation.
        alternatives (iterable[iterable[str]]): Use alternate symbols.
            Mostly useful in conjunction with ROMAN_ALTERNATIVES
        signed (bool): Accept negative numbers.
            The minus symbol is then prepended to string for negative numbers.
            No symbol is added for positive numbers.
        negative_sign (str): The symbol to use for negative numbers.
            The negative sign will be the first character of the representation.

    Returns:
        text (str): The converted Roman number.
            By default the dedicated uppercase Unicode characters are used.
            This can be tweaked through the appropriate options.

    Examples:
        >>> [int2roman(i) for i in range(13)]
        ['N', 'Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ', 'Ⅹ', 'Ⅺ', 'Ⅻ']
        >>> [int2roman(i) for i in range(13, 23)]
        ['ⅩⅢ', 'ⅩⅣ', 'ⅩⅤ', 'ⅩⅥ', 'ⅩⅦ', 'ⅩⅧ', 'ⅩⅨ', 'ⅩⅩ', 'ⅩⅪ', 'ⅩⅫ']
        >>> [int2roman(i) for i in [44, 51, 62, 73, 84, 95, 99]]
        ['ⅩⅬⅣ', 'ⅬⅠ', 'ⅬⅫ', 'ⅬⅩⅩⅢ', 'ⅬⅩⅩⅩⅣ', 'ⅬⅩⅬⅤ', 'ⅬⅩⅬⅨ']
        >>> [int2roman(i) for i in range(1666, 3999, 517)]
        ['ⅯⅮⅭⅬⅩⅥ', 'ⅯⅯⅭⅬⅩⅩⅩⅢ', 'ⅯⅯⅮⅭⅭ', 'ⅯⅯⅯⅭⅭⅩⅦ', 'ⅯⅯⅯⅮⅭⅭⅩⅩⅩⅣ']
        >>> [int2roman(i) for i in range(-1666, 1666, 639)]
        ['-ⅯⅮⅭⅬⅩⅥ', '-ⅯⅩⅩⅦ', '-ⅭⅭⅭⅬⅩⅩⅩⅧ', 'ⅭⅭⅬⅠ', 'ⅮⅭⅭⅭⅬⅩⅬ', 'ⅯⅮⅩⅩⅨ']
        >>> [int2roman(k * 10 ** i) for i in range(3, 6) for k in [4, 5, 10]]
        ['Ⅿↁ', 'ↁ', 'ↂ', 'ↂↇ', 'ↇ', 'ↈ', 'ↈↇↃ', 'ↇↃ', 'ⅭↈↃ']
        >>> [int2roman(2 ** i) for i in range(14, 17)]
        ['ↂↁⅯⅭⅭⅭⅬⅩⅩⅩⅣ', 'ↂↂↂⅯⅯⅮⅭⅭⅬⅩⅧ', 'ↇↂↁⅮⅩⅩⅩⅥ']
        >>> [int2roman(i, only_ascii=True) for i in [1666, 3999, 4000, 189000]]
        ['MDCLXVI', 'MMMDCDLXLIX', 'MDO', 'CCCDOODOOCCDOCCDOCCDODOMDO']
        >>> [int2roman(i, only_additive=True) for i in [4, 49, 949, 9494]]
        ['ⅡⅡ', 'ⅩⅩⅩⅩⅦⅡ', 'ⅮⅭⅭⅭⅭⅩⅩⅩⅩⅦⅡ', 'ↁⅯⅯⅯⅯⅭⅭⅭⅭⅬⅩⅩⅩⅩⅡⅡ']
        >>> [int2roman(i, extended=False) for i in range(3995, 4001)]
        Traceback (most recent call last):
            ....
        ValueError: `4000` needs `extended` option
        >>> [int2roman(i, uppercase=False) for i in range(1666, 5000, 631)]
        ['ⅿⅾⅽⅼⅹⅵ', 'ⅿⅿⅽⅽⅼⅹⅼⅶ', 'ⅿⅿⅾⅽⅾⅹⅹⅷ', 'ⅿⅿⅿⅾⅼⅸ', 'ⅿⅾↄⅽⅼⅹⅼ', 'ⅿⅾↄⅾⅽⅽⅽⅹⅺ']
        >>> [int2roman(i, claudian=True) for i in [1666, 3999, 4000, 189000]]
        ['ⅯⅮⅭⅬⅩⅥ', 'ⅯⅯⅯⅮⅭⅮⅬⅩⅬⅨ', 'ⅯⅮↃ', 'ⅭⅭↀↃↃⅮↃↃⅭↀↃⅭↀↃⅭↀↃⅮↃⅯⅮↃ']
        >>> [int2roman(i, alternatives=ROMAN_ALTERNATIVES)
        ...  for i in [6, 50, 1000, 56, 1006, 1050, 1056, 1057]]
        ['ↅ', 'ↆ', 'ↀ', 'ↆↅ', 'ↀↅ', 'ↀↆ', 'ↀↆↅ', 'ↀↆⅦ']
        >>> [int2roman(i, signed=False) for i in [1666, -1666]]
        Traceback (most recent call last):
            ....
        ValueError: `-1666` needs `signed` option
    """
    text = ''
    # update max_consecutive
    max_consecutive = _ROMAN_MAX_CONSECUTIVE[only_additive]
    # handles negative numbers
    if num < 0:
        if signed:
            text += negative_sign
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
        compound_over10 = (11, 12)
        while num > 0:
            if num < max_standard * (max_consecutive + 1):
                for val, key in _ROMAN_UNICODE_R.items():
                    if val and num - val >= 0 and val not in compound_over10:
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
                    prev_key = key if val not in compound_over10 else prev_key
            elif extended:
                # max_apostrophus = max(_ROMAN_APOSTROPHUS.values())
                min_apostrophus = min(_ROMAN_APOSTROPHUS.values())
                log_m = math.log10(min_apostrophus)
                log_num = math.log10(num)
                is_half = num >= 5 * 10 ** int(log_num)
                repeat = int(log_num) - int(log_m) + (1 if is_half else 0)
                num_to_add = (5 if is_half else 1) * 10 ** int(log_num)
                correction = -2 * num_to_add \
                    if num >= num_to_add * (max_consecutive + 1) else 0
                char_to_append = ('Ⅾ' if is_half else (
                    'Ⅽ' * repeat + ('ↀ' if repeat else 'Ⅿ'))) + 'Ↄ' * repeat
                if not claudian:
                    char_to_append = multi_replace(
                        char_to_append, _ROMAN_CLAUDIAN_TO_APOSTROPHUS)
                text += char_to_append
                num -= num_to_add + correction
            else:
                raise ValueError('`{}` needs `extended` option'.format(num))
    # ensure use of compact chars for 11 and 12
    text = multi_replace(text, (('ⅩⅠ', 'Ⅺ'), ('ⅩⅡ', 'Ⅻ')))
    if only_additive:
        text = multi_replace(text, (('Ⅳ', 'ⅡⅡ'), ('Ⅸ', 'ⅦⅡ')))
    if alternatives:
        text = multi_replace(text, alternatives)
    if only_ascii:
        text = multi_replace(text, _ROMAN_UNICODE_TO_ASCII)
    if not uppercase:
        text = multi_replace(text, _ROMAN_CLAUDIAN_TO_APOSTROPHUS_R).lower()
    else:  # should not be necessary
        text = text.upper()
    return text


# ======================================================================
def roman2int(
        text,
        strict=False,
        strict_regex=_ROMAN_STRICT_REGEX,
        negative_sign=_ROMAN_MINUS):
    """
    Convert a string representation of a Roman number to integer.

    Args:
        text (str): The input number to parse.
        strict (bool): Only accept strictly formally valid Roman numbers.
            The following is checked:
            - repetition of identical symbols more than 3 times not allowed,
              except for apostrophus notation.
            - the symbols are sorted according decreasing value left-to-right,
              except for the subtraction notation, which allow a single
              symbol of next lower value to be placed on the left of a larger
              value symbol (this is to avoid the necessity for repeating the
              same symbol 4 times).
        strict_regex (str): The regular expression defining formal correctness.
            This must be a valid expression accepted by Python's `re.match()`.
            If `strict` is False, this parameter is ignored.
        negative_sign (str): The symbol to use for negative numbers.
            The negative sign must be the first character of the representation.

    Returns:
        num (int): The integer represented.

    Notes:
        - Large numbers using the apostrophus notation cannot be parsed yet,
          but if no apostrophus notation is used (and strict parsing is not set)
          the parsing works.

    Examples:
        >>> [roman2int(s) for s in ['MDCLXVI', 'iv', 'Ⅵ', 'IC', 'IIM', 'VL']]
        [1666, 4, 6, 99, 998, 45]
        >>> invalid = 0
        >>> for s in ['MDCLXVI', 'IC', 'IIM', 'VL', 'MDO', 'CCDCCDOCCDODOMDO']:
        ...     try:
        ...         roman2int(s, strict=True)
        ...     except ValueError:
        ...         invalid += 1
        ...     except NotImplementedError:
        ...         pass
        1666
        >>> print('Invalid: {}'.format(invalid))
        Invalid: 3
        >>> roman2int('MMMMMM')
        6000
        >>> roman2int('MMMMMM', strict=True)
        Traceback (most recent call last):
            ....
        ValueError: Formally invalid input `MMMMMM`
        >>> [roman2int(s) for s in ['CCDO', 'DO']]
        Traceback (most recent call last):
            ....
        NotImplementedError: Cannot parse large numbers yet!
        >>> all([i == roman2int(int2roman(i)) for i in range(-3999, 4000, 7)])
        True
        >>> all([i == roman2int(int2roman(i)) for i in range(1666, 10000, 973)])
        Traceback (most recent call last):
            ....
        NotImplementedError: Cannot parse large numbers yet!
    """
    num = None
    text = text.strip().upper()
    if negative_sign in text and text[0] == negative_sign:
        sign = -1
        text = text[1:]
    else:
        sign = 1
    text = multi_replace(text, _ROMAN_UNICODE_TO_ASCII)
    text = multi_replace(text, tuple([(i, j) for (j, i) in ROMAN_ALTERNATIVES]))
    valid_chars = set(''.join([a for u, a in _ROMAN_UNICODE_TO_ASCII]))
    if set(text).issubset(valid_chars):
        num = 0
        if text != _ROMAN_ASCII_R[0]:
            is_valid = re.match(strict_regex, text)
            if _ROMAN_ASCII_R[0] in text:
                raise ValueError(
                    'Invalid: if `{}` in input, cannot contain else'.format(
                        _ROMAN_ASCII_R[0]))
            elif _ROMAN_CLAUDIAN_TO_ASCII in text:
                raise NotImplementedError('Cannot parse large numbers yet!')
            elif not strict or is_valid:
                for i, char in enumerate(text):
                    if i + 1 < len(text) and any(
                            [_ROMAN_ASCII[tmp_char] > _ROMAN_ASCII[char]
                             for tmp_char in text[i + 1:]]):
                        num -= _ROMAN_ASCII[char]
                    else:
                        num += _ROMAN_ASCII[char]
            else:
                raise ValueError('Formally invalid input `{}`'.format(text))
    else:
        raise ValueError('Input contains invalid characters')
    return sign * num


# ======================================================================
def main():
    print(__doc__.strip())
    doctest.testmod()


# ======================================================================
if __name__ == '__main__':
    main()
