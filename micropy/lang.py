# -*- coding: utf-8 -*-
# yapf

import ast
import inspect
import patterns
import funcy
import types
import copy
import numbers
import funcy
from functools import singledispatch
from pysistence import Expando
from typing import Any, Mapping

import itertools
from functools import partial, wraps, update_wrapper

from micropy import primitives

PRIMTYPES = {int, bool, float, str, set, list, tuple, dict}

textual = funcy.isa(str)
numeric = funcy.isa(numbers.Number)
isint = funcy.isa(int)
isdict = funcy.isa(dict)


def typename(x):
    # type: (Any) -> str
    """Safely get a type name from parameter `x`. If `x == None` returns
    `'None'`

    """
    return x is None and 'None' or x.__class__.__name__


class XE(Expando):
    def __getitem__(self: 'XE', attr: str) -> Any:
        "Support for getting attributes as named string indexes"
        return getattr(self, attr)

    def iteritems(self: 'XE') -> Mapping[str, Any]:
        # type: (self) -> None
        "Does iteritems"
        return self.to_dict().items()

    def get(self, name, default=None):
        return self.to_dict().get(name, default)


def pubvars(obj):
    # type: (Any) -> Iterable
    "Returns all public variables except methods"
    if isdict(obj):
        return obj.keys()
    else:
        return [
            attr for attr in dir(obj)
            if not attr.startswith('__') and not callable(getattr(obj, attr))
        ]


def isprimitive(obj):
    # type: (Any) -> bool
    "Determines if a value belongs to a primitive type (= {numbers, strings})"

    if numeric(obj):
        return True
    elif textual(obj):
        return True

    return False


def isprim_type(type_):
    # type: (type_) -> None
    "Does primtype"
    return True if type_ in PRIMTYPES else False


def tolerant_or_original(Exc, fn):
    # type: (Exception, Callable) -> None
    """Returns a function that will allow the Exception(s) in `Exc` to
    occur."""
    def invoke(obj):
        # type: (obj) -> None
        "Does invoke"
        try:
            return fn(obj)
        except Exc:
            return obj

    return invoke


def coerce_or_same(T: Any) -> str:
    "Special case of `tolerant_or_original()` for type coercion."
    "Does coerce_or_same"
    return tolerant_or_original((TypeError, ValueError, AttributeError), T)


maybe_int = coerce_or_same(int)


def methdispatch(func):
    # type: (Callable) -> Callable
    """Thanks Zero Piraeus!

    https://stackoverflow.com/a/24602374/288672
    """
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


class Undefined:
    "Marker class for undefined values."


def primbases(cls):
    # type: (type) -> Any
    "Does primbase"
    return [T for T in cls.__bases__ if isprim_type(T)]


def primitve_instance(cls, *params, **opts):
    # type: (cls, *args, **kwargs) -> Any
    "Does acts_as_primitve"
    primparams = [v for v in params if isprim_type(type(v))]
    instance = PrimType.__new__(cls, *primparams, **opts)
    instance.prim_type = PrimType
    return instance


def bind_methods(Base, instance):
    # type: (instance, Base) -> None
    "Does bind_methods"
    for name, fn in instance.__bind__:
        setattr(Base, name, types.MethodType(fn, instance))
    return instance


__classmethod__ = classmethod
__staticmethod__ = staticmethod


class Base(object):
    __bind__ = []

    def __init__(self, *params, **opts):
        bind_methods(self.__class__, self)

        def bind_method_on_self(self, fn):
            # type: () -> None
            "Does bound_on_instance"

            name = fn.__name__

            @wraps(fn)
            def callit(*params, **opts):
                # type: (*params, **opts) -> None
                "Does callit"
                return fn(self, *params, **opts)

            setattr(self, name, callit)
            return callit

        self.method = types.MethodType(bind_method_on_self, self)

    @__staticmethod__
    def __wrapper(fn, Cls=None, name=None):
        # type: () -> None
        "Does __wrapper"
        if name is None:
            name = fn.__name__

        @wraps(fn)
        def do_call(*params, **opts):
            if Cls is None:
                return fn(*params, **opts)
            else:
                return fn(*((Cls, ) + params), **opts)

        if Cls is None:
            setattr(Base, name, do_call)
        else:
            setattr(Cls, name, do_call)

        return do_call

    @__classmethod__
    def classmethod(cls, fn):
        return Base.__wrapper(fn, Cls=cls)

    @__staticmethod__
    def staticmethod(fn):
        return Base.__wrapper(fn)

    @__classmethod__
    def method(Subclass, fn):
        # type: (fn) -> None
        "Creates a method from the decorated function `fn`"
        setattr(Subclass, fn.__name__, types.MethodType(fn, Subclass))
        return fn


def mkclass(name, bases=(), **clsattrs):
    # type: (str, Tuple[Any, Any]) -> Any
    "Does mkclass"

    Gen = type(name, (Base, ) + bases, clsattrs)
    return Gen
