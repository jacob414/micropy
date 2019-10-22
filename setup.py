#!/usr/bin/env python
# yapf

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import distutils.cmd

import micropy


class QACommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self: 'QACommand') -> None:
        pass

    def finalize_options(self: 'QACommand') -> None:
        pass

    def run(self: 'QACommand') -> None:
        print('run qa..')


install = (
    "funcy>=1.10.2",
    "pysistence>=0.4.1",
    "patterns>=0.3",
    "jsonpickle>=1.2",
)  # yapf: disable

develop = (
    "pytest>=5.0.1",
    "hypothesis>=4.24.3",
    "altered_states>=1.0.9",
)  # yapf: disable

setup(
    name='micropy',
    cmdclass={
        'qa': QACommand,
    },
    version=micropy.__version__,
    description="Some Python nicieties",
    packages=('micropy', ),
    author='Jacob Oscarson',
    author_email='jacob@414soft.com',
    install_requires=install,
    extras_require={
        'test': install + develop,
    },
    license='MIT',
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
