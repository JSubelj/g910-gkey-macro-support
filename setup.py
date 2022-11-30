#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup
import lib.PROJECT_INFO as PROJECT_INFO

# Package meta-data.
NAME = PROJECT_INFO.NAME
DESCRIPTION = PROJECT_INFO.DESCRIPTION
URL = PROJECT_INFO.URL
EMAIL = PROJECT_INFO.EMAIL
AUTHOR = PROJECT_INFO.AUTHOR
REQUIRES_PYTHON = PROJECT_INFO.REQUIRES_PYTHON
VERSION = PROJECT_INFO.VERSION

# What packages are required for this module to be executed?
REQUIRED = [
    "python-uinput==0.11.2", "pyusb==1.0.2"
]


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {'__version__': VERSION}

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    # If your package is a single module, use this instead of 'packages':
    py_modules=['cli_entry_point'],

    entry_points={
        'console_scripts': ['g910-gkeys=cli_entry_point:main'],
    },
    install_requires=REQUIRED,
    # extras_require=EXTRAS,
    include_package_data=True,
    license='GPL3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
    # $ setup.py publish support.
    cmdclass={
    },
)
