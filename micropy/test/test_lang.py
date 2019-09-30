# -*- coding: utf-8 -*-
# -*- yapf -*-

import pytest

from micropy import lang
from micropy.testing import fixture
from hypothesis import given, example, strategies as st
import _ast


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
    "Should "

    @Alt.classmethod
    def cmeth(cls, x, y):
        # type: (cls) -> None
        "Does cmeth"
        return x + y

    sum = Alt.cmeth(1, 1)
    assert sum == 2, \
        "Expected 2, got {}".format(sum)


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


@fixture.params("type_, expected",
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
)  # yapf: disable
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
