# -*- coding: utf-8 -*-
# encoding: utf-8
# -----------------------------------------------------------------------------
# Copyright (C) 2017 Glooko, Inc https://www.glooko.com/
# -----------------------------------------------------------------------------
"""
Test support for Analyzer py.test unit tests.
"""

# "51* == [51, [511,512]]

import ast


class Op:
    def __init__(self, term):
        self.term = term

    def calc(self):
        for step in self.ops:
            yield lambda value: step(value)
        # return lambda value: self.do(self.value, self.prior)

    def is_a(self, other):
        # type: (self, other) -> None
        "Does is_a"
        return isinstance(other, self.__class__)


class Eq(Op):
    def __eq__(self, value):
        return value == self.term


class Has(Op):
    def __contains__(self, element):
        return element in self.term


class And(Op):
    def __and__(self, other):
        return calc()

class Or(Op):
    def __or__(self, other):
        # type: (self, other) -> None
        "Does __or__"
        return self.__class__(other, self)

class Kind(Op):
    def __eq__(self, other):
        # type: () -> None
        "Does __e"
        return isinstance(other, self.term)


def Q(query):
    # type: (bag, query) -> None
    """Makes and wraps one query.

    Hyp. example:
    Q(p(node == assign) & p(node.value == list) & p(node.targes[-1].value.id == 'TestVariables') & p(len(node.value.elts) == 1))
    """
    yield query.run()


if __name__ == '__main__':
    # tree = ast.parse('foo.py')
    has = Has('backports.lzma')
    assert 'lzma' in has
    assert 'foobar' not in has
    assert Kind(list) == []
    assert Kind(list) == [1,2,3]
    assert not Kind(list) == ()
    assert not Kind(list) == (1,2,3)

