# -*- coding: utf-8 -*-
import patterns
from patterns import helpers
from altered import E
import astor

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
        print(f'Visiting def {node.name}')
        self.generic_visit(node)

    def visit_Call(self, node):
        # import ipdb; ipdb.set_trace()
        print(f'Visiting call {node.func.id}')
        self.generic_visit(node)


def transform(visitor):
    # type: (VisitorCls) -> None
    "Does transform"
    def visit_(fn):
        root = astor.code_to_ast(fn)
        import ipdb; ipdb.set_trace()
        visitor.visit(root)

    return visit_

def fn():
    return None


@transform(FuncLister())
def entry():
    # type: () -> None
    "Does entry"
    fn()
    return 'entry'

