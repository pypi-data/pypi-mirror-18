#!/usr/bin/env python3

import os
from setuptools import setup

from morinkit import __version__, __author__, __license__, __url__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

long_desc = 'For more information, visit the GitHub repository: {}'.format(__url__)

requires = read('requirements.txt').rstrip().split("\n")
tests_requires = read('requirements-tests.txt').rstrip().split("\n")


setup(
    name='morinkit',
    version=__version__,
    description='Python functions for cancer genomics',
    long_description=long_desc,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics'],
    keywords='bioinformatics cancer genomics utility tool',
    author=__author__,
    author_email='morinlab@sfu.ca',
    url=__url__,
    license=__license__,
    packages=['morinkit'],
    entry_points={'console_scripts': ['morinkit = morinkit.morinkit:main']},
    install_requires=requires,
    test_suite='tests',
    tests_require=tests_requires)
