# -*- coding: utf-8 -*-
import patterns
from patterns import helpers
from copy import copy

import ast

def messing():
    print('rad 1')
    print(foo)
    return 'returvärde'

def alien():
    print('alien 1!')
    print('alien 2!')
    foo = 'bar'

if __name__ == '__main__':
    tree = patterns.get_ast(messing)
    body = tree.body[0].body
    # call = ast.Expr(value=helpers.make_call('alien'))

    abody = patterns.get_ast(alien).body
    idx = 0
    for stmnt in abody[0].body:
        body.insert(idx, stmnt)
        idx += 1

    # body.insert(0, abody[0].body[0])

    local = {}
    ast.fix_missing_locations(tree)
    code = compile(tree, 'foo', 'single')
    eval(code, {}, local)

    local['messing']()

