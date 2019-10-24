#!/usr/bin/env python
# yapf

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import micropy

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

try:
    # make setup.py review available only to fully dev-capable
    # interpreter instances
    import mypy

    from micropy.testing import ReviewProject
    cmdclass = {'review': ReviewProject}
except ImportError:
    cmdclass = {}

setup(
    name='micropy',
    cmdclass=cmdclass,
    version=micropy.__version__,
    description="Some Python nicieties",
    packages=('micropy', ),
    author='Jacob Oscarson',
    author_email='jacob@414soft.com',
    install_requires=install,
    extras_require={
        'test': install + develop,
    },
    url='https://www.414soft.com/micropy',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
