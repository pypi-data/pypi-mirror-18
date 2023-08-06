[![PyPI version](https://badge.fury.io/py/script2package.svg)](https://badge.fury.io/py/script2package)

script2package
==============

script2package is a Python script which converts a single python script into a package which can then be installed via `python setup.py install`.

Usage: `script2package script.py --base base_folder`

To extend the flexibility of this package, you can enable setup options through
providing `setup.cfg` if you so desire.

Installation
============

You can install this package via `pip` (`pip install script2package`) or `python setup.py install`.

Examples
========

A bootstrap example has been provided by running `script2package script2package.py`, which will produce a self contained version within the folder `package`.

A simple standalone example with no `setup.cfg` file is provided in `Example/add/add.py` with the generated package in `Example/add/package`.



