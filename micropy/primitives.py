# yapf

import inspect
import ast
import sys

from typing import Any, List, Callable, Union, Collection

from collections.abc import Iterable

import funcy
from funcy import flow


def pipe(invalue, *chain):
    # type: (Any, List[Callable]) -> Any
    val = chain[0](invalue)

    for step in chain[1:]:
        val = step(val)

    return val


class PipingExperiment(object):
    """An experiment pushing the pipe concept a bit longer. Not sure where
    I'm going with this but curious.

    """
    def __init__(self, seed):
        # type: (Any) -> PipingExperiment
        self.result = seed

    def __or__(self, step):
        # type: (Callable) -> PipingExperiment
        self.result = step(self.result)
        return self


P = PipingExperiment


def raises(ExcType):
    # type: (Exception) -> Callable
    """Returns a function that will raise an exception of specified type
    when called. The exception receives the called functions
    parameters.

    """
    def raiser(*args, **kwargs):
        raise ExcType(*args, **kwargs)

    return raiser


IT = type(int)
itrt = Iterable


def empty_ob(o: Any) -> bool:
    "Does empty_ob"
    return o is object and len(o.__dict) == 0


def func_file(func):
    return getattr(sys.modules[func.__module__], '__file__', '<nofile>')


def nanoast(obj):
    # type: (obj) -> None
    "Does nanoast"
    source = inspect.getsource(obj)
    return ast.parse(source, func_file(obj), 'single')


NarrowingPredicate = Union[Any, Callable[[Any], bool]]


class Narrowable(object):
    def narrow(self, pred: NarrowingPredicate) -> 'Narrowable':
        # type: (NarrowingPredicate) -> Narrowable

        if callable(pred):
            # Narrow by a callabale predicate
            pred_ = flow.ignore(Exception, False)(pred)
            return narrowable(self.base([el for el in self if pred_(el)]))

        else:
            # Narrow by exact match
            return narrowable(self.base([el for el in self if pred == el]))

    def __getitem__(self, idx: Union[Any, NarrowingPredicate]) -> Narrowable:
        "Finds individual node in itself or searches.."
        try:
            return narrowable(super().__getitem__(idx))
        except TypeError:
            return self.narrow(idx)
        except KeyError:
            return self.narrow(idx)
        except IndexError:
            return self.narrow(idx)


def narrowable(src: Union[Any, Collection]) -> Narrowable:
    "Creates the base class an initializes a Narrowable collection."

    class Narrower(Narrowable, src.__class__):
        base = src.__class__

    return Narrower(src)
