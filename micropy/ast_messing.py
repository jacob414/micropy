# -*- coding: utf-8 -*-
import patterns
from patterns import helpers
from altered import E

import ast


def third():
    print('third')


def messing():
    print('rad 1')
    print(foo)


def alien():
    print('alien 1!')
    print('alien 2!')
    third()
    foo = 'bar'


def eval_(tree, name='expanded'):
    code = compile(tree, 'name', 'single')
    local = {}
    eval(code, globals(), local)
    return (v for v in local.values())


if __name__ == '__main__':
    import ipdb
    ipdb.set_trace()