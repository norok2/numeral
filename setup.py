#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup instructions.

See: https://packaging.python.org/en/latest/distributing.html
"""

# ======================================================================
# :: Future Imports (for Python 2)
from __future__ import (
    division, absolute_import, print_function, unicode_literals)

# ======================================================================
# :: Python Standard Library Imports
import os  # Miscellaneous operating system interfaces
import re  # Regular expression operations
from codecs import open  # use a consistent encoding (in Python 2)

# ======================================================================
# :: Choice of the setup tools
from setuptools import setup
from setuptools import find_packages

# ======================================================================
# project specific variables
VERSION_FILEPATH = 'numeral/numeral.py'
README_FILEPATH = 'README.rst'

# get the working directory for the setup script
CWD = os.path.realpath(os.path.dirname(__file__))

# get the long description from the README file
with open(os.path.join(CWD, README_FILEPATH), encoding='utf-8') as readme_file:
    LONG_DESCRIPTION_TEXT = readme_file.read()


# ======================================================================
def fix_version(
        version=None,
        source_filepath=VERSION_FILEPATH):
    """
    Fix version in source code.

    Args:
        version (str): version to be used for fixing the source code
        source_filepath (str): Path to file where __version__ is located

    Returns:
        version (str): the actual version text used
    """
    if version is None:
        import setuptools_scm

        version = setuptools_scm.get_version()
    with open(source_filepath, 'r') as src_file:
        src_str = src_file.read().decode('utf-8')
        src_str = re.sub(
            r"__version__ = '.*'",
            "__version__ = '{}'".format(version),
            src_str, flags=re.UNICODE)

    with open(source_filepath, 'w') as src_file:
        src_file.write(src_str.encode('utf-8'))

    return version


# ======================================================================
# :: call the setup tool
setup(
    name='numeral',

    description='Support for various integer-to-numeral (and back) conversion.',
    long_description=LONG_DESCRIPTION_TEXT,

    # use_scm_version=True,
    version=fix_version(),

    url='https://bitbucket.org/norok2/numeral',

    author='Riccardo Metere',
    author_email='rick@metere.it',

    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',

        'Natural Language :: English',
        'Natural Language :: Latin',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Scientific/Engineering',
        'Topic :: Sociology :: History',
        'Topic :: Education',
        'Topic :: Utilities',

        'Operating System :: POSIX',

        'License :: OSI Approved :: GNU General Public License v3 or later'
        ' (GPLv3+)',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    keywords=('numeral', 'letter', 'alphabet', 'numeric', 'arabic', 'roman'),

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    setup_requires=[
        'setuptools',
        'setuptools_scm'
    ],

    extras_require={
        'blessed': 'blessed',
    },

    entry_points={
        'console_scripts': [
            'numeral=numeral.numeral:main',
        ],
    },
)
