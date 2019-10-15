# -*- coding: utf-8 -*-
# -*- yapf -*-

import pytest

from micropy import lang
from micropy.testing import fixture
from hypothesis import given, example, strategies as st
import _ast

from typing import Any


@pytest.fixture
def Dispatcher():
    class Dispatching(object):
        @lang.methdispatch
        def reflect(self, arg):
            raise NotImplementedError("Not implemented for {}".format(
                type(arg)))

        @reflect.register(list)
        def _(self, alist):
            return (list, alist)

        @reflect.register(int)
        def _(self, anint):
            return (int, anint)

    yield Dispatching


def test_methdispatch(Dispatcher):
    # type: () -> None
    "Should dispatch per type"
    assert Dispatcher().reflect([1, 2]) == (list, [1, 2])


@pytest.fixture
def Alt():
    # type: () -> None
    "Does Alt"
    yield lang.mkclass('Alt')


def test_mkclass_classmethod(Alt):
    # type: () -> None
    "Should be able to declare dynamic class methods"

    @Alt.classmethod
    def cmeth(cls, x, y):
        # type: (cls) -> None
        "Does cmeth"
        return x + y

    sum = Alt.cmeth(1, 1)
    assert sum == 2, \
        "Expected 2, got {}".format(sum)


def test_mkclass_staticmethod(Alt):
    # type: () -> None
    "Should be able to declare dynamic class methods"

    @Alt.staticmethod
    def smeth(x, y):
        # type: (cls) -> None
        "Does cmeth"
        return x + y

    sum = Alt.smeth(1, 1)
    assert sum == 2, \
        "Expected 2, got {}".format(sum)


def test_method_on_type_0param(Alt: Alt) -> None:
    # type: () -> None
    "Should handle methods without parameters correctly"

    @Alt.method
    def paramless_method(self: Alt):
        "An example parameterless method"
        self.foo = id(self)

    alt0 = Alt()
    alt0.paramless_method()
    assert type(alt0.foo) is int


def test_method_on_type_nary(Alt: Alt) -> None:
    # type: () -> None
    "Should"

    @Alt.method
    def meth_on_type(self: Alt, foo: Any):
        "Does meth_on_type"
        self.foo = foo

    alt0 = Alt()
    alt0.meth_on_type('bar')
    assert alt0.foo == 'bar'


def test_mkclass_bound_method(Alt: Alt) -> None:
    "Should be able to add methods to individual objects."
    alt1, alt2 = Alt(), Alt()

    @alt1.method
    def amethod(self, foo):
        # type: (foo) -> None
        "Does _"
        self.bar = foo + 1

    alt1.amethod(1)
    assert alt1.bar == 2
    assert not hasattr(alt2, 'amethod')


@fixture.params(
    "type_, expected",
    (int, True),
    (bool, True),
    (float, True),
    (str, True),
    (set, True),
    (list, True),
    (dict, True),
    (object, False),
    ('', False),
    (1, False),
)
def test_isprim_type(type_, expected):
    # type: () -> None
    "Should work"
    assert lang.isprim_type(type_) == expected


int_or_same = lang.coerce_or_same(int)


@fixture.params("value, expected", (1, 1), ('1', 1), ('x', 'x'))
def test_coerce_or_same(value, expected):
    # type: () -> None
    "Should convert strings with digits to `int`."
    assert int_or_same(value) == expected


@pytest.fixture
def xe():
    yield lang.XE(foo='foo', bar='bar')


def test_xe_as_obj(xe):
    # type: () -> None
    "Should "
    assert xe.foo == 'foo'


def test_xe_as_dict(xe):
    # type: (P.XE) -> None
    "Should be able to index XE object as dictionaries"
    assert xe['foo'] == 'foo'
