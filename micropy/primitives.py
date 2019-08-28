from itertools import islice
import inspect

from pysistence import Expando


def head(gen):
    # type: (Generator) -> Generator[Any, Any, Any]
    "Convenience function to pick the head element from a generator object ('car')"
    try:
        return next(gen)

    except StopIteration:
        return None


def tail(gen):
    # type: (Generator) -> Generator[Any, Any, Any]
    return islice(gen, 1, None)


def pipe(invalue, *chain):
    # type: (Any, List[Callable]) -> Any
    val = head(iter(chain))(invalue)

    for step in tail(chain):
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


class XE(Expando):
    __getitem__ = lambda self, attr: getattr(self, attr)
    iteritems = lambda self: self.to_dict().iteritems()

    def __init__(self, mapping):
        # type: (XE, dict) -> None
        super().__init__(**mapping)

    def get(self, name, default=None):
        return self.to_dict().get(name, default)
