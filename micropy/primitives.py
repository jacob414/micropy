# yapf

import inspect
import re
import inspect
import ast
import sys
from itertools import islice

from collections.abc import Iterable

from pysistence import Expando
from pysistence.expando import make_expando_class

from . import lang


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


def f(str_):
    """
    Poor man's f-strings (e.g. if you are stuck on Python 2).

    Caller `locals()` expansion technique, thanks Gareth Rees,
    http://stackoverflow.com/a/6618825/288672
    """

    frame = inspect.currentframe()
    try:
        return str_.format(**frame.f_back.f_locals)

    finally:
        del frame


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

empty_ob = lambda o: o is object and len(o.__dict) == 0


class LWO(object):
    def __init__(self, *args, **kw):
        self.__dict__.update(**kw)

    def has(self, fn):
        # typse: (fn) -> None
        "Does meth"

        def invoke(*args, **kw):
            # type: () -> None
            "Does wrap"
            res = fn(*args, **kw)
            return res

        setattr(self, fn.__name__, invoke)
        return invoke


def explore(obj, name=None, level=0):
    # type: (obj) -> None
    "Does explore"
    rendered = ''

    if name is None:
        name = '{}<{}>'.format(obj.__class__.__name__, str(id(obj)))
    if level is 0:
        rendered += '{}\n'.format(name)
        level += 1
    indent = 2 * level * ' '
    for attr, value in obj.__dict__.items():
        rendered += indent + "{attr} = {value!r}\n".format(**locals())

    return rendered


def func_file(func):
    return getattr(sys.modules[func.__module__], '__file__', '<nofile>')


def nanoast(obj):
    # type: (obj) -> None
    "Does nanoast"
    source = inspect.getsource(obj)
    # source = re.sub(r'(^|\n)' + spaces, '\n', source)
    # if spaces:
    #     source = re.sub(r'(^|\n)' + spaces, '\n', source)
    return ast.parse(source, func_file(obj), 'single')


class XE(Expando):
    """Thin convenience wrapper around Pysistence's Expando class. Makes
    the Expando appear as both `dict` and `object`.

    """

    __getitem__ = lambda self, attr: getattr(self, attr)
    iteritems = lambda self: self.to_dict().iteritems()

    def get(self, name, default=None):
        return self.to_dict().get(name, default)
