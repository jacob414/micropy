# yapf

import inspect
import ast
import sys

from typing import Any, List, Callable

from collections.abc import Iterable


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
