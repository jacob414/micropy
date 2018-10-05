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

def apply(tree, name='expanded'):
    code = compile(tree, 'name', 'single')
    local = {}
    xx = eval(code, globals(), local)
    return (v for v in local.values())

if __name__ == '__main__':
    tree = patterns.get_ast(messing)
    body = tree.body[0].body

    abody = patterns.get_ast(alien).body
    idx = 0
    for stmnt in abody[0].body:
        body.insert(idx, stmnt)
        idx += 1

    for x in apply(tree):
        x()

