# yapf
import pytest

from micropy import primitives as P


def incr(x: int) -> int:
    return x + 1


def test_pipe0():
    # type: () -> None
    "Should "
    assert P.pipe(10, incr, incr) == 12


def test_pipe_experiment():
    # type: () -> None
    "Should 1. add 1, 2. add 1, 3. profit?"
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
