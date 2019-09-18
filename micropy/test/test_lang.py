# -*- coding: utf-8 -*-
# -*- yapf -*-

import pytest

from micropy import lang
from micropy.testing import fixture
from hypothesis import given, example, strategies as st
import _ast


@pytest.mark.skip
@given(st.text())
@example('if')
@example('for')
def test_node_sane(name):
    # type: () -> None
    "Should "
    try:
        node = lang.node(name)
        assert compile(node, 'name', 'single')
    except KeyError:
        pass


def inline(x):
    100
    101


def test_body():
    # type: () -> None
    "Should poc"
    xx = lang.body(inline)
    assert tuple(exp.value.n for exp in xx) == (100, 101)


@pytest.mark.skip
def test_lispify():
    # type: () -> None
    "Does test_lispify"
    lang.nodemap[_ast.Str](None)


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
