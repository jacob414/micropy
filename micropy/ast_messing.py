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


class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(f'Visiting {node.name}..')
        self.generic_visit(node)


def transform(VisitorCls):
    # type: (VisitorCls) -> None
    "Does transform"
    def visit_(fn):
        xx = patterns.get_ast(fn)
        FuncLister().visit(xx)

    return visit_


@transform(FuncLister)
def entry():
    # type: () -> None
    "Does entry"
    return 'entry'

