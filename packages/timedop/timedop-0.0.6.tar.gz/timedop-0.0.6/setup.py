#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TimedOp Setup

-Christopher Welborn 12-04-2016
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Default README files to use for the longdesc, if pypandoc fails.
readmefiles = ('docs/README.txt', 'README.txt', 'docs/README.rst')
for readmefile in readmefiles:
    try:
        with open(readmefile, 'r') as f:
            longdesc = f.read()
        break
    except EnvironmentError:
        # File not found or failed to read.
        pass
else:
    # No readme file found.
    defaultdesc = 'Time python operations or enforce a time limit for calls.'
    # If a README.md exists, and pypandoc is installed, generate a new readme.
    try:
        import pypandoc
    except ImportError:
        print('Pypandoc not installed, using default description.')
        longdesc = defaultdesc
    else:
        # Convert using pypandoc.
        try:
            longdesc = pypandoc.convert('README.md', 'rst')
        except EnvironmentError:
            # No readme file, no fresh conversion.
            print('Pypandoc readme conversion failed, using default desc.')
            longdesc = defaultdesc


shortdesc = 'Time python operations or enforce a time limit for calls.'
try:
    with open('DESC.txt', 'r') as f:
        shortdesc = f.read()
except FileNotFoundError:
    pass


setup(
    name='timedop',
    version='0.0.6',
    author='Christopher Welborn',
    author_email='cj@welbornprod.com',
    packages=['timedop'],
    url='http://pypi.python.org/pypi/TimedOp/',
    description=shortdesc,
    long_description=longdesc,
    keywords=('python module library 2 3 ...'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
