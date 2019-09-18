# yapf
import pytest
from hypothesis import given, example, strategies as st

from micropy import primitives as P


def test_pipe0():
    # type: () -> None
    "Should "
    afn = lambda x: x + 1
    bfn = lambda x: x + 2
    assert P.pipe(10, afn, bfn) == 13


def test_pipe_experiment():
    # type: () -> None
    "Should 1. add 1, 2. add 1, 3. profit?"
    incr = lambda x: x + 1
    showr = "It is {}!".format

    assert (P.PipingExperiment(5) | incr | incr | showr).result == "It is 7!"


class ExceptionType(Exception):
    def __init__(self, msg, **kw):
        self.message = msg
        self.__dict__.update(**kw)


def test_raises_by_type():
    # type: () -> None
    "Should create a raising function"
    with pytest.raises(ExceptionType) as excinfo:
        P.raises(ExceptionType)('foo', bar='baz')

    exc = excinfo.value

    assert exc.message == 'foo'
    assert exc.bar == 'baz'


@pytest.fixture
def xe():
    yield P.XE(foo='foo', bar='bar')


def test_xe_as_obj(xe):
    # type: () -> None
    "Should "
    assert xe.foo == 'foo'


def test_xe_as_dict(xe):
    # type: (P.XE) -> None
    "Should be able to index XE object as dictionaries"
    assert xe['foo'] == 'foo'
