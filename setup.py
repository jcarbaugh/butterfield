#!/usr/bin/env python
# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

# from butterfield import __appname__, __version__
from setuptools import setup

long_description = open('README.md').read()

setup(
    # name       = __appname__,
    # version    = __version__,
    name       = "butterfield",
    version    = "0.1",
    packages   = ['butterfield'],

    install_requires = [
        "websockets==2.3",
        "slacker==0.8.7",
    ],
    dependency_links=[
        "https://github.com/gfreezy/slacker/tarball/master#egg=slacker-0.8.7",
    ],
    entry_points = {'console_scripts': [
        'butterfield = butterfield.cli:main'
    ]},

    author       = "Sunlight Foundation",
    author_email = "labs@sunlightfoundation.com",

    long_description = long_description,
    description      = '',
    license          = "BSD",
    url              = "https://github.com/sunlightlabs/butterfield",

    platforms        = ['any']
)
