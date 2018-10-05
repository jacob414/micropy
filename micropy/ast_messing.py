# -*- coding: utf-8 -*-
import patterns
from patterns import helpers
from copy import copy

import ast

def messing(x):
    print('rad 1')
    return 'returvärde'

def alien():
    print('alien 1!')

if __name__ == '__main__':
    tree = patterns.get_ast(messing)
    body = tree.body[0].body
    call = ast.Expr(value=helpers.make_call('alien'))

    abody = patterns.get_ast(alien).body
    body.insert(0, abody[0].body[0])

    # body.insert(0, call)

    local = {}
    ast.fix_missing_locations(tree)
    code = compile(tree, 'foo', 'single')
    eval(code, {'alien': alien}, local)

    print(local['messing'](1))

