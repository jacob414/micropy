# -*- coding: utf-8 -*-
# yapf

import pytest

from micropy import lang
from micropy.testing import fixture, logcall

from typing import Any
import operator as ops


@pytest.fixture
def rgen() -> None:
    "A fixture with a recursive generator expression"
    return (e for e in (1,
                        2,
                        (e for e in range(31, 34)),
                        4,
                        (e for e in range(51, 54))))  # yapf: disable


def test_unfold_gen(rgen) -> None:
    "Should unfold a recursive generator correctly."
    assert lang.unfold_gen(rgen) == (1, 2, 31, 32, 33, 4, 51, 52, 53)


class Dispatching(object):
    @lang.methdispatch
    def reflect(self, arg):
        raise NotImplementedError("Not implemented for {}".format(type(arg)))

    @reflect.register(list)
    def _(self, alist):
        return (list, alist)

    @reflect.register(int)
    def _(self, anint):
        return (int, anint)


@pytest.fixture
def Dispatcher():
    yield Dispatching


def test_methdispatch(Dispatcher: Dispatching) -> None:
    "Should dispatch per type"
    assert Dispatcher().reflect([1, 2]) == (list, [1, 2])


@pytest.fixture
def Alt():
    "Does Alt"
    yield lang.mkclass('Alt')


def test_mkclass_classmethod(Alt: Any) -> None:
    "Should be able to declare dynamic class methods"

    @Alt.classmethod
    def cmeth(cls, x, y) -> int:
        "Does cmeth"
        return x + y

    sum = Alt.cmeth(1, 1)
    assert sum == 2, \
        "Expected 2, got {}".format(sum)


def test_mkclass_staticmethod(Alt: Any) -> None:
    "Should be able to declare dynamic class methods"

    @Alt.staticmethod
    def smeth(x, y):
        "Does cmeth"
        return x + y

    sum = Alt.smeth(1, 1)
    assert sum == 2, \
        "Expected 2, got {}".format(sum)


def test_method_on_type_0param(Alt: Alt) -> None:
    "Should handle methods without parameters correctly"

    @Alt.method
    def paramless_method(self: Alt):
        "An example parameterless method"
        self.foo = id(self)

    alt0 = Alt()
    alt0.paramless_method()
    assert type(alt0.foo) is int


def test_method_on_type_nary(Alt: Alt) -> None:
    "Should"

    @Alt.method
    def meth_on_type(self: Alt, foo: str):
        "Does meth_on_type"
        self.foo = foo

    alt0 = Alt()
    alt0.meth_on_type('bar')
    assert alt0.foo == 'bar'


def test_mkclass_bound_method(Alt: Alt) -> None:
    "Should be able to add methods to individual objects."
    alt1, alt2 = Alt(), Alt()

    @alt1.method
    def amethod(self: Alt, foo: int):
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
def test_isprim_type(type_: type, expected: Any) -> None:
    "Should work"
    assert lang.isprim_type(type_) == expected


int_or_same = lang.coerce_or_same(int)


@fixture.params("value, expected", (1, 1), ('1', 1), ('x', 'x'))
def test_coerce_or_same(value: Any, expected: Any) -> None:
    "Should convert strings with digits to `int`."
    assert int_or_same(value) == expected


@pytest.fixture
def xe() -> lang.XE:
    yield lang.XE(foo='foo', bar='bar')


def test_xe_as_obj(xe: lang.XE) -> None:
    "Should "
    assert xe.foo == 'foo'


def test_xe_as_dict(xe: lang.XE) -> None:
    "Should be able to index XE object as dictionaries"
    assert xe['foo'] == 'foo'


@pytest.fixture
def simplest_pipe() -> lang.Piping:
    "A fixture with a Piping object that only supports add."

    class SimplestPipe(lang.Piping):
        def __add__(self, value) -> None:
            "Does __add__"
            self.queue(ops.add, value)
            return self

    return SimplestPipe(10)


def test_piping_simplest(simplest_pipe) -> None:
    "Should piping_simplest"
    res = simplest_pipe + 10 + 20
    assert res() == 40


@pytest.mark.xfail(raises=NotImplementedError)
def test_piping_simplest_restrictive(simplest_pipe) -> None:
    "Should piping_simplest_restrictive1"
    simplest_pipe + 10 - 20


class FilterPipeExample(lang.Piping):
    def __add__(self, value) -> lang.Piping:
        "Add operation"
        self.queue(ops.add, value)
        return self


@fixture.params("fpipe, param, want",
  (FilterPipeExample(8,
                     kind=filter,
                     format=logcall(lambda x: x > 10, 'over10')),
   (8, 9, 10, 11, 12),
   (11,12)
))  # yapf: disable
def test_piping_as_filter(fpipe: FilterPipeExample, param: tuple,
                          want: tuple) -> None:
    """Piping object should be able to work as filters provided a
    formattting function is specified.

    """
    # fpipe, = fpipe
    # import ipdb
    # ipdb.set_trace()
    # pass
    with logcall.on():
        fpipe + 1
        assert fpipe.state == 'fresh'
        res0 = fpipe(8)
        assert fpipe.state == 'post first run'
        assert res0 is False
        assert fpipe.now == (9, )
        fpipe + 1
        res1 = fpipe(9)
        assert res1 is False
        assert fpipe(8) is False
        assert fpipe.now == (10, )
        assert fpipe.state == 'post first run'
        was = tuple(filter(fpipe, param))
        assert was == want


def test_piping_as_mapping() -> None:
    """Piping objects derived from `ComposePiping` should always support
    the bitwise pipe (`'|'`) operatror as a simple function
    composition.

    """
    incr = lambda x: x + 1
    showr = "It is {}!".format
    assert (lang.ComposePiping(5) >> incr >> incr >> showr)() == "It is 7!"
