hdu: Human-friendly summary of disk usage
=========================================

This software computes an estimate of the file disk usage for files and
directories, similarly to the UNIX program 'du'.
The result is then displayed to the console in a human friendly format.

It includes the following features:

- a progress bar of each item for quick visual inspection
- percentage information (precision can be set)
- show the size of each item in the specified units
- support for SI, IEC and UNIX ('du') units
- maximum depth (of the displayed items) can be specified
- optionally follow symlinks, mount points, special files and hidden files
- can filter results to display only directories
- can output results ending with '\\0' instead of newlines (useful for parsing)
- can sort results by name or by size

Installation
------------
The recommended way of installing the software is through
`PyPI <https://pypi.python.org/pypi/hdu>`_:

.. code:: shell

    $ pip install hdu

Alternatively, you can the clone the source repository from
`Bitbucket <https://bitbucket.org/norok2/hdu>`_:

.. code:: shell

    $ mkdir hdu
    $ cd hdu
    $ git clone git@bitbucket.org:norok2/hdu.git
    $ python setup.py install

(last step may require additional permissions depending on your configuration)

The software does not have additional dependencies beyond Python and its
standard library.

It was tested with Python 2.7 and 3.5.
Other version were not tested.

Note
----
Although the software is ready, the packaging is still experimental.
If you experience any issues, please consider reporting it.
Suggestions and improvements are welcome!

