numeral: support for various integer-to-numeral (and back) conversion
=====================================================================

This Python library implements integer-to-numeral and numeral-to-integer
conversion for a variety of numeral representations, including:

- alphabetic representation, i.e. a, b, c, d, ... for 0, 1, 2, 3, ...
- Roman numbers, i.e. I, II, III, IV, ... for 1, 2, 3, 4, ...
- generic tokens set representation, i.e. !, @, !!, !@, ... for 0, 1, 2, 3...
  (given the tokens set {``!``, ``@``}).

The generic tokens set representation uses the least number of tokens for
representing a given integer, and uses an exponential-like notation similar to
base-n conversion, except that the first symbol is used.
The alphabetic representation is a special case of a generic tokens set
representation, where the latin alphabet is used as tokens set.
Upper/lower case conversion should be handled through Python built-ins.
All representation support negative values.

Detailed documentation is available for all functions through docstrings.

Of note, the Roman numbers support include:

- both **Unicode** and **ASCII-only** representations
- partial support for large numbers via the so-called Apostrophus notation
  (see: `<https://en.wikipedia.org/wiki/Roman_numerals#Apostrophus>`_)
- additive-only or subtractive notations
- toggleable forgiving/strict Roman number parsing
- representation of zero
  (see: `<https://en.wikipedia.org/wiki/Roman_numerals#Zero>`_)
- negative numbers (with option to specify a custom negative sign)
- partial support for archaic/late forms
  (see: `<https://en.wikipedia.org/wiki/Numerals_in_Unicode#Roman_numerals>`_)


Installation
------------
The recommended way of installing the software is through
`PyPI <https://pypi.python.org/pypi/numeral>`_:

.. code:: shell

    $ pip install numeral

Alternatively, you can clone the source repository from
`Bitbucket <https://bitbucket.org/norok2/numeral>`_:

.. code:: shell

    $ mkdir numeral
    $ cd numeral
    $ git clone git@bitbucket.org:norok2/numeral.git
    $ python setup.py install

(some steps may require additional permissions depending on your configuration)

The software does not have additional dependencies beyond Python and its
standard library.

It was tested with Python 2.7 and 3.5.
Other version were not tested.


Usage
-----

The following functions are defined:

int2letter
~~~~~~~~~~
Convert a number to the least amount letters (within an alphabet).

.. code:: python

    >>> int2letter(10)
    'k'
    >>> import string  # Common string operations
    >>> int2letter(10, string.ascii_letters)  # using both lower and upper cases
    'aW'

letter2int
~~~~~~~~~~
Convert a group of letters (within a given alphabet) to a number.

.. code:: python

    >>> letter2int('aa')
    26


int2tokens
~~~~~~~~~~
Convert a number to the least amount tokens (within a tokens set).


.. code:: python

    >>> int2tokens(12, ('!', '@', '#', '$'))
    '#!'


tokens2int
~~~~~~~~~~
Convert a group of tokens (within a given set) to a number.

.. code:: python

    >>> tokens2int('#!', ('!', '@', '#', '$'))
    12


int2roman
~~~~~~~~~
Convert an integer to its corresponding Roman number representation.

.. code:: python

    >>> int2roman(1666)  # using dedicated unicode chars
    'ⅯⅮⅭⅬⅩⅥ'
    >>> int2roman(1666, only_ascii=True)  # using only ASCII
    'MDCLXVI'


roman2int
~~~~~~~~~
Convert a string representation of a Roman number to integer.

.. code:: python

    >>> int2roman('MDCLXVI')
    1666


