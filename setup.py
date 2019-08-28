#!/usr/bin/env python
# yapf

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import micropy

__version__ = '0.5.0'
install_requires = {
    "funcy>=1.10.2",
    'pysistence>=0.4.1',
}

setup(
    name='micropy',
    version=micropy.__version__,
    description="Some Python nicieties",
    package=('micropy', ),
    author='Jacob Oscarson',
    author_email='jacob@414soft.com',
    install_requires=install_requires,
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
