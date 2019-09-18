#!/usr/bin/env python
# yapf

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
import micropy

install = (
    "funcy>=1.10.2",
    "pysistence>=0.4.1",
    "patterns>=0.3"
)  # yapf: disable

develop = (
    "pytest>=5.0.1",
)  # yapf: disable

if sys.version_info.major < 3:
    from micropy import depend_2019
    install = install + depend_2019.backports

setup(
    name='micropy',
    version=micropy.__version__,
    description="Some Python nicieties",
    package=('micropy', ),
    author='Jacob Oscarson',
    author_email='jacob@414soft.com',
    install_requires=install,
    extras_require={
        'test': install + develop,
    },
    test_require=install + develop,
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
