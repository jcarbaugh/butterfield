#!/usr/bin/env python
# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

from butterfield import __appname__, __version__
from setuptools import setup

long_description = open('README.md').read()

setup(
    name       = __appname__,
    version    = __version__,
    packages   = ['butterfield'],

    install_requires = [
        "slacker",
        "requests==2.5.0",
        "websockets==2.3",
    ],

    entry_points = {'console_scripts': [
        'butterfield = butterfield.cli:main'
    ]},

    author       = "Jeremy Carbaugh",
    author_email = "jcarbaugh@sunlightfoundation.com",

    long_description = long_description,
    description      = '',
    license          = "BSD",
    url              = "https://github.com/sunlightlabs/butterfield",

    platforms        = ['any']
)
