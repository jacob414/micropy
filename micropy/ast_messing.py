# -*- coding: utf-8 -*-
import patterns
from patterns import helpers
from copy import copy

import ast

def messing(x):
    print('rad 1')
    return 'returvärde'

def alien():
    print('alien!')

if __name__ == '__main__':
    tree = patterns.get_ast(messing)
    body = tree.body[0].body
    cand = body[-1]
    cand.value.s = 'changed!'
    call = ast.Expr(value=helpers.make_call('alien'))
    body.insert(0, call)
    ast.fix_missing_locations(tree)
    local = {}
    code = compile(tree, 'foo', 'single')
    eval(code, {'alien': alien}, local)
    print(local['messing'](1))

