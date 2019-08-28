from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='micropy',
    version='0.1',
    description='Tiny Python toolkit',
    install_requires=['Funcy', "patterns"],
    extras_require={
        'dev': [],
        'test': ["pytest>=3.2.3", "mock", "altered.states",
                 "pytest-cov", "mypy>=0.550"],
    },
    entry_points={
        'console_scripts': [
            'py.test = pytest:main [test]',
        ],
    },
)
