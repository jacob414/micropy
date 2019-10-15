# -*- coding: utf-8 -*-
# yapf

import ast
import inspect
import patterns
import funcy
import types
import copy
import typing
import numbers
import funcy
from functools import singledispatch
from pysistence import Expando

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
    __getitem__ = lambda self, attr: getattr(self, attr)
    iteritems = lambda self: self.to_dict().iteritems()

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

    if numeric(obj): return True
    elif textual(obj): return True

    return False


def isprim_type(type_):
    # type: (type_) -> None
    "Does primtype"
    return True if type_ in PRIMTYPES else False


def tolerant_or_original(Exc, fn):
    # type: (Exception, Callable) -> None
    """Returns a function that will allow the Exception(s) in `Exc` to occur."""
    def invoke(obj):
        # type: (obj) -> None
        "Does invoke"
        try:
            return fn(obj)
        except Exc:
            return obj

    return invoke


coerce_or_same = lambda T: tolerant_or_original(
    (TypeError, ValueError, AttributeError), T)
"Special case of `tolerant_or_original()` for type coercion."

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

    def def_method_on_instance(self, fn):
        # type: () -> None
        "Does def_method_on_instance"

        def method_call_on_future_instance(*params, **opts):
            return fn(*params, **opts)

        return method_call_on_future_instance

    @__classmethod__
    def method(Subclass, fn):
        # type: (fn) -> None
        "Creates a method from the decorated function `fn`"
        sig = inspect.signature(fn)
        name = fn.__name__
        params = dict(sig.parameters.items())
        arity = len(params)

        self_instance = None

        if arity > 0 and 'self' in params:
            # is a method

            def method_call_on_future_instance(*params, **opts):
                if self_instance:
                    params = (self_instance, ) + params
                return fn(*params, **opts)

            # Subclass = fn.__globals__[fn.__globals__['name']]

            mw = fn.__hash__  # should always be there
            xx = [
                x for x in mw.__self__.__globals__ if isinstance(x, Subclass)
            ]

            for name_ in mw.__self__.__globals__.keys():
                if isinstance(mw.__self__.__globals__[name_], Subclass):
                    if name_ in mw.__self__.__globals__:
                        self_instance = mw.__self__.__globals__[name_]

            if self_instance and mw.__self__.__globals__:
                instance_or_type = self_instance
                print(self_instance)
                self_instance
                print(f'Instance {instance_or_type} found for method {name}')
                setattr(instance_or_type, name,
                        types.MethodType(fn, self_instance))
            else:
                # no instance in scope above
                instance_or_type = Subclass
                print('Interpreted as subclass, proceed with that')
                Subclass.__bind__.append(
                    (fn.__name__, method_call_on_future_instance))
                setattr(Subclass, name, method_call_on_future_instance)

        elif arity == 0:
            Base.__bind__.append((fn.__name__, fn))
            setattr(Base, name, method_call_on_future_instance)

        return fn


def mkclass(name, bases=(), **clsattrs):
    # type: (str, Tuple[Any, Any]) -> Any
    "Does mkclass"

    Gen = type(name, (Base, ) + bases, clsattrs)
    return Gen


# pprint(primitives.explore(argsbuild(('foo', 'bar'), hello='world')))

# POC 9:e feb
# from micropy import lang

# def re_eval(top, globals_=None):
#     recompiled = compile(top, 'mame', 'single')
#     if globals_ is None:
#         globals_ = globals()
#     env = {}
#     eval(recompiled, globals(), env)
#     first, = env.values()
#     return first

# def foo():
#     # type: () -> None
#     "Does foo"
#     (1 + 3) / 2

# nodes = lang.body(foo)
# n0, n1 = nodes
# n1.value.n = 2

# print(lang.eval_(nodes, foo)())

# In [52]: %%dump_ast
#    ....: @dec1
#    ....: @dec2
#    ....: def f(a: 'annotation', b=1, c=2, *d, e, f=3, **g) -> 'return annotation':
#    ....:   pass
#    ....:
# Module(body=[
#     FunctionDef(name='f', args=arguments(args=[
#         arg(arg='a', annotation=Str(s='annotation')),
#         arg(arg='b', annotation=None),
#         arg(arg='c', annotation=None),
#       ], vararg=arg(arg='d', annotation=None), kwonlyargs=[
#         arg(arg='e', annotation=None),
#         arg(arg='f', annotation=None),
#       ], kw_defaults=[
#         None,
#         Num(n=3),
#       ], kwarg=arg(arg='g', annotation=None), defaults=[
#         Num(n=1),
#         Num(n=2),
#       ]), body=[
#         Pass(),
#       ], decorator_list=[
#         Name(id='dec1', ctx=Load()),
#         Name(id='dec2', ctx=Load()),
#       ], returns=Str(s='return annotation')),
#   ])
