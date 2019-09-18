# yapf

from itertools import islice
import inspect

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


try:
    from collections.abc import Iterable
except ImportError:
    # Have patience dear frends, this too will pass.
    from collections import Iterable

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


#        if atomic(value):
#            rendered += indent + "{attr} = {value!r}\n".format(**locals())ode
#        else:
#            rendered += explore(value, level=level + 1)

    return rendered


def climb(obj, path):
    # type: (Any, Optional[*int, Iterable, Generator]) -> Any
    "Does climb"
    # climb([1,2,[3,4],5], 2) -> (3,4)
    # climb([1,2,[3,4],5], [2, 0]) -> 3
    # climb([1,2,[3,4],5], [2, 1]) -> 4
    # climb([1,2,[3,4],5], [2, 2]) -> raise Missing

    raise NotImplementedError()


import re
import inspect
import ast
import sys


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


def f1(x):
    # type: (x) -> None
    "Does f1"
    return x + 1


f1_ = nanoast(f1)


class Cls:
    pass


Cls_ = nanoast(Cls)


class XE(Expando):
    """Thin convenience wrapper around Pysistence's Expando class. Makes
    the Expando appear as both `dict` and `object`.

    """

    __getitem__ = lambda self, attr: getattr(self, attr)
    iteritems = lambda self: self.to_dict().iteritems()

    def get(self, name, default=None):
        return self.to_dict().get(name, default)
