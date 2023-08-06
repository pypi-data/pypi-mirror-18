#!/usr/bin/env python
# -*- coding: utf-8 -
#
# This file is part of SatAPI released under the GPLv3 license.

from setuptools import setup, find_packages

import glob
from imp import load_source
import os
import sys

extras = {}

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries']

SCRIPTS = []

def main():
    version = load_source("version", os.path.join("satapi",
        "version.py"))

    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()

    DATA_FILES = [
        ('satapi', ["LICENSE", "README.rst", "THANKS", "TODO.txt"])
        ]

    options=dict(
            name = 'satapi',
            version = version.__version__,
            description = 'Satellite 6 API REST module',
            long_description = long_description,
            author = 'Sergio G.',
            author_email = 'soukron@gmbros.net',
            license = 'GPLv3',
            url = 'http://github.com/soukron/satapi2',
            classifiers = CLASSIFIERS,
            packages = find_packages(exclude=['tests']),
            data_files = DATA_FILES,
            scripts = SCRIPTS,
            zip_safe =  False,
            install_requires = [
                'restkit>=4.2.2',
                'config>=0.3.9'],
        )


    setup(**options)

if __name__ == "__main__":
    main()
