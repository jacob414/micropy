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
from . import pipelib

from functools import wraps, update_wrapper, reduce

PRIMTYPES = {int, bool, float, str, set, list, tuple, dict}
LISTLIKE = {set, list, tuple}

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
    "Returns the number of arguments required by `fn`."
    return len(inspect.signature(fn).parameters)


always_tup = funcy.iffy(funcy.complement(funcy.is_seqcont), lambda x: (x, ))


class Piping(pipelib.BasePiping):
    """Piping objects is for (ab)using Python operator overloading to
    build small pipeline-DSL's.

    The most basic one will simply refuse to do anything - you have to
    give it instructions/permissions on everything it's made for ;-).

    """
    class Fresh(object):
        "Marker for Piping instances that never has been run"
        pass

    class Executed(object):
        "Marker for Piping instances that has been run"
        pass

    def __init__(self,
                 seed: Union[tuple, Any] = (),
                 kind: Callable = map,
                 format: Callable[[Any, None, None], Any] = funcy.identity):
        self.cursor = ()
        self.ops = ()
        self.results = {}
        self.last_result = ()

        self.format = format
        self.kind = kind

        self.seed = always_tup(seed)

    def sum(self) -> None:
        "Does show"
        print(self.__class__.__name__)
        textual = (
            f'kind = {self.kind}, state = {self.state}, seed = {self.seed}, cursor = {self.cursor}, last result = {self.last_result}'
        )
        print(textual)

    @property
    def now(self):
        return self.last_result

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
        self.ops = (*self.ops, ((stepf, x)))
        return self

    def run(self, seed, *x: Any) -> None:
        "Does do"
        self.cursor = seed
        for op, operands in self.ops:
            if operands:
                self.cursor = op(*(self.cursor, *operands))
            else:
                self.cursor = op(self.cursor)
        return self.cursor

    @property
    def state(self):
        if self.cursor == () and self.last_result == ():
            return Piping.Fresh
        elif self.last_result != ():
            return Piping.Executed

        raise ValueError('Piping: undeterminable state')

    def calc_fmt_param(self, kind, res, params, case):
        # case = (self.kind, ) + self.seed + self.ops
        if kind is filter and self.state == Piping.Fresh:
            # This case is logically obsolete but good for readability.
            return (res, )
        elif self.kind is filter:
            # Always compares against call parameters
            return params
        elif kind is map or kind == 'pipe':
            return (res, )

        raise TypeError('Piping: unknown out parameter scenario')

    def __call__(self, *params: Any) -> Any:
        """Treating the Pipe as a function calculates the Pipe's result and
        returns it passed through the return formatting function.

        Unary calls for pipelined function composition behavoiour,
        binary calls to combine a value with the result of the pipe
        operations (map/filter/reduce).

        """

        # Calculate case
        case = (self.kind, ) + self.seed + self.ops

        # Decide on operands for this run
        if self.state == Piping.Fresh:
            # When the pipeline must be run, prefer parameter but
            # otherwise seed
            operands = params or self.seed
        else:
            # When a result exist, prefer seed
            operands = self.seed or params

        # An incorrectly handled pipe is a possibility here
        if not operands:
            raise ValueError('Piping: fatal/undeterminable operands')

        try:
            # Stored, grab this case from results storage
            res = self.results[case]
        except KeyError:
            # This case has not been stored yet
            res = self.run(*operands)

            # On success:
            # Store last result in tuple form
            self.last_result = always_tup(res)
            # Also store the Piping case.
            self.results[case] = res

        # Decide on return format
        format_params = self.calc_fmt_param(self.kind, res, params, case)
        # Invoke return format function with parameter(s) from above
        return self.format(*format_params)


class ComposePiping(Piping):
    """Common usage of Piping - the >> operator is the simplest possible
    function composition. I decided against the | operator since it's
    needed for logical pipes.

    Most implementations will probably be based of this.

    """
    def __rshift__(self, stepf: Callable[[Any, None, None], Any]) -> None:
        "Bitwise OR as simple function composition"
        return self.queue(stepf)
