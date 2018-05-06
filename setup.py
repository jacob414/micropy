#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import micropy


setup(
    name='micropy',
    version=micropy.__version__,
    description="Some Python nicieties",
    package=('micropy',),
    author='Jacob Oscarson',
    author_email='jacob@414soft.com',
    licence='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License (MIT)',
        'Operating System :: OS Independent',
    ],
)
