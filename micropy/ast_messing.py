# -*- coding: utf-8 -*-
import patterns
from patterns import helpers
from altered import E
import astor
import inspect
import types

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
        self.generic_visit(node)

    def visit_Call(self, node):
        self.generic_visit(node)


def transform(visitor):
    # type: (VisitorCls) -> None
    "Does transform"

    def visit_(fn):
        root = astor.code_to_ast(fn)
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


code = astor.code_gen.to_source

X = ast.Expression
ld = ast.Load
BO = ast.BinOp
N = lambda name: ast.Name(id=name)
nn = ast.Num
EQ = ast.Eq

#print(code(BO(BO(N('foo'), ast.Add(), ast.Num(1)), ast.Add(), ast.Num(2))))


class Exp(object):
    @property
    def code(self):
        return code(self.ast)

    @property
    def exp(self):
        return ast.fix_missing_locations(ast.Expression(self.ast))

    def apply(self):
        return eval(compile(self.exp, 'x', 'eval'))


class Var(object):
    def __init__(self, name='x'):
        self.name = name

    @property
    def node(self):
        return ast.Name(id=self.name, ctx=ast.Load())


class Op(Exp):
    def opr(Op_, Term):
        def do(self, x):
            val = getattr(x, 'node', Term(x))
            self.ast = BO(self.ast, Op_(), val)
            return self

        return do

    def __init__(self, val):
        self.ast = ast.Num(val)
        super().__init__()

    __add__ = opr(ast.Add, ast.Num)
    __sub__ = opr(ast.Sub, ast.Num)
    __mul__ = opr(ast.Mult, ast.Num)
    __truediv__ = opr(ast.Div, ast.Num)
    __floordiv__ = opr(ast.FloorDiv, ast.Num)
    __mod__ = opr(ast.Mod, ast.Num)


x = Op(1)

x + Var()

print(x.code)
# print(x.apply())
# exp = Op(1) + 2 + 3
# print(exp.code)
# print(exp.apply())
