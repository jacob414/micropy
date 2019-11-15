# -*- coding: utf-8 -*-
# yapf

import funcy
import types
import numbers
from functools import singledispatch
from functools import lru_cache
from pysistence import Expando
from typing import Any, Mapping, List, Tuple, Iterable, Generator, Callable, Union
import inspect

from functools import wraps, update_wrapper, reduce

PRIMTYPES = {int, bool, float, str, set, list, tuple, dict}

textual = funcy.isa(str)
numeric = funcy.isa(numbers.Number)
isint = funcy.isa(int)
isdict = funcy.isa(dict)
isgen = funcy.isa(types.GeneratorType)


def unfold_gen(x: Generator[Any, None, None],
               cast: type = tuple) -> Iterable[Any]:
    """Quick recursive unroll of possibly nested (uses funcy library under
    the hood)

    """
    return cast(funcy.flatten(x, isgen))


def typename(x: Any) -> str:
    """Safely get a type name from parameter `x`. If `x == None` returns
    `'None'`

    """
    return x is None and 'None' or x.__class__.__name__


class XE(Expando):
    def __getitem__(self: 'XE', attr: str) -> Any:
        "Support for getting attributes as named string indexes"
        return getattr(self, attr)

    def iteritems(self: 'XE') -> Mapping[str, Any]:
        "Does iteritems"
        return self.to_dict().items()

    def get(self, name, default=None):
        return self.to_dict().get(name, default)


def pubvars(obj: Any) -> Iterable:
    "Returns all public variables except methods"
    if isdict(obj):
        return obj.keys()
    else:
        return [
            attr for attr in dir(obj)
            if not attr.startswith('__') and not callable(getattr(obj, attr))
        ]


def isprimitive(obj):
    "Determines if a value belongs to a primitive type (= {numbers, strings})"

    if numeric(obj):
        return True
    elif textual(obj):
        return True

    return False


def isprim_type(type_):
    "Does primtype"
    return True if type_ in PRIMTYPES else False


def tolerant_or_original(Exc, fn):
    """Returns a function that will allow the Exception(s) in `Exc` to
    occur."""
    def invoke(obj) -> Any:
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
    "Does primbase"
    return [T for T in cls.__bases__ if isprim_type(T)]


def bind_methods(Base, instance):
    "Does bind_methods"
    for name, fn in instance.__bind__:
        setattr(Base, name, types.MethodType(fn, instance))
    return instance


__classmethod__ = classmethod
__staticmethod__ = staticmethod


class Base(object):
    __bind__: List[Tuple[Callable, Any]] = []

    def __init__(self, *params, **opts):
        bind_methods(self.__class__, self)

        def bind_method_on_self(self: Any, fn: Callable):
            "Does bound_on_instance"

            name = fn.__name__

            @wraps(fn)
            def callit(*params: Any, **opts: Any) -> None:
                "Does callit"
                return fn(self, *params, **opts)

            setattr(self, name, callit)
            return callit

        self.method = types.MethodType(bind_method_on_self, self)

    @__staticmethod__
    def __wrapper(fn: Callable, Cls: Any = None, name: str = None):
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
    def staticmethod(fn: Callable) -> Callable:
        return Base.__wrapper(fn)

    @__classmethod__
    def method(Subclass: Any, fn: Callable) -> Callable:
        "Creates a method from the decorated function `fn`"
        setattr(Subclass, fn.__name__, types.MethodType(fn, Subclass))
        return fn


def mkclass(name: str, bases: Tuple = (), **clsattrs: Any) -> Any:
    "Does mkclass"

    Gen = type(name, (Base, ) + bases, clsattrs)
    return Gen


def arity(fn: Callable) -> int:
    "Does arity"
    return len(inspect.signature(fn).parameters)


class Piping(object):
    """Piping objects is for (ab)using Python operator overloading to
    build small pipeline-DSL's.

    The most basic one will simply refuse to do anything - you have to
    give it instructions/permissions on everything it's made for ;-)."""

    stepf_arity = {
        map: 1,
        filter: 1,
        reduce: 2,
    }

    def __init__(self,
                 seed: Union[tuple, Any] = (),
                 kind: Callable = map,
                 format: Callable[[Any, None, None], Any] = None):
        self.cursor = self.seed = tuple(funcy.flatten(() + (seed, )))
        if format is None:
            self.format = funcy.identity
        else:
            self.format = format

        self.kind = kind
        self.ops = []

    def fncompose(self, stepf: Callable[[Any, None, None], Any],
                  x: Any = None) -> 'Piping':
        operands = arity(stepf)
        if operands == 1:
            operand = ()  # only return value from previous step function
        elif operands == 2:
            operand = (x, )

        self.queue(stepf, x)
        return self

    def queue(self, stepf: Callable[[Any, Any, None], Any], *x: Any) -> None:
        "Does queue"
        cursor = self.cursor  # at time of queue
        self.ops.append((stepf, x))
        return self

    # @lru_cache(maxsize=1, typed=True)
    def run(self, seed, *x: Any) -> None:
        "Does do"
        self.cursor = seed
        for op, operands in self.ops:
            if operands:
                self.cursor = op(*(self.cursor, *operands))
            else:
                self.cursor = op(self.cursor)
        return self.cursor

    def __call__(self, *params: Any) -> Any:
        operands = getattr(self, 'seed', params)
        if not operands:
            raise ValueError('undeterminable first operands')
        res = self.run(*operands)
        if self.seed == () and params != () and self.kind is filter:
            # First run case
            return self
        elif self.kind is filter:
            # Always compares against call parameters
            res = self.format(*params)
            return res
        elif self.kind is map:
            return self.format(res)
        else:  # filter case
            return self.format(*params)
        # return self.format(intermediate)
        # return self.format(*params)
        # return self.format(*combo)

    def __add__(self, other):
        raise NotImplementedError('Does not implement +')

    def __sub__(self, other):
        raise NotImplementedError('Does not implement -')

    def __mul__(self, other):
        raise NotImplementedError('Does not implement *')

    def __matmul__(self, other):
        raise NotImplementedError('Does not implement @')

    def __truediv__(self, other):
        raise NotImplementedError('Does not implement /')

    def __floordiv__(self, other):
        raise NotImplementedError('Does not implement //')

    def __mod__(self, other):
        raise NotImplementedError('Does not implement %')

    def __divmod__(self, other):
        raise NotImplementedError('Does not implement divmod')

    def __pow__(self, other, modulo=None):
        raise NotImplementedError('Does not implement pow')

    def __lshift__(self, other):
        raise NotImplementedError('Does not implement <<')

    def __rshift__(self, other):
        raise NotImplementedError('Does not implement >>')

    def __and__(self, other):
        raise NotImplementedError('Does not implement &')

    def __xor__(self, other):
        raise NotImplementedError('Does not implement ^')

    def __or__(self, other):
        raise NotImplementedError('Does not implement |')

    def __radd__(self, other):
        raise NotImplementedError('Does not implement righthand +')

    def __rsub__(self, other):
        raise NotImplementedError('Does not implement righthand -')

    def __rmul__(self, other):
        raise NotImplementedError('Does not implement righthand *')

    def __rmatmul__(self, other):
        raise NotImplementedError('Does not implement righthand @')

    def __rtruediv__(self, other):
        raise NotImplementedError('Does not implement righthand /')

    def __rfloordiv__(self, other):
        raise NotImplementedError('Does not implement rightand %')

    def __rmod__(self, other):
        raise NotImplementedError('Does not implement righthand %')

    def __rdivmod__(self, other):
        raise NotImplementedError('Does not implement righthand divmod')

    def __rpow__(self, other):
        raise NotImplementedError('Does not implement righthand pow')

    def __rlshift__(self, other):
        raise NotImplementedError('Does not implement righthand +')

    def __rrshift__(self, other):
        raise NotImplementedError('Does not implement righthand +')

    def __rand__(self, other):
        raise NotImplementedError('Does not implement righthand +')

    def __rxor__(self, other):
        raise NotImplementedError('Does not implement righthand +')

    def __ror__(self, other):
        raise NotImplementedError('Does not implement righthand +')

    def __iadd__(self, other):
        raise NotImplementedError('Does not implement +=')

    def __isub__(self, other):
        raise NotImplementedError('Does not implement -=')

    def __imul__(self, other):
        raise NotImplementedError('Does not implement *=')

    def __imatmul__(self, other):
        raise NotImplementedError('Does not implement +')

    def __itruediv__(self, other):
        raise NotImplementedError('Does not implement +')

    def __ifloordiv__(self, other):
        raise NotImplementedError('Does not implement +')

    def __imod__(self, other):
        raise NotImplementedError('Does not implement %=')

    def __ipow__(self, other, modulo=None):
        raise NotImplementedError('Does not implement **=')

    def __ilshift__(self, other):
        raise NotImplementedError('Does not implement <<=')

    def __irshift__(self, other):
        raise NotImplementedError('Does not implement >>=')

    def __iand__(self, other):
        raise NotImplementedError('Does not implement +')

    def __ixor__(self, other):
        raise NotImplementedError('Does not implement +')

    def __ior__(self, other):
        raise NotImplementedError('Does not implement +')

    def __neg__(self):
        raise NotImplementedError('Does not implement +')

    def __pos__(self):
        raise NotImplementedError('Does not implement +')

    def __abs__(self):
        raise NotImplementedError('Does not implement +')

    def __invert__(self):
        raise NotImplementedError('Does not implement +')

    def __int__(self):
        return int(self.result)

    def __float__(self):
        raise float(self.result)


class ComposePiping(Piping):
    """Common usage of Piping - the | operator is the simplest possible
    function composition.

    Most implementations will probably be based of this.

    """
    def __or__(self, stepf: Callable[[Any, None, None], Any]) -> None:
        "Bitwise OR as simple function composition"
        return self.queue(stepf)
