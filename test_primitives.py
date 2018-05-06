import pytest

from micropy import primitives as P


@pytest.fixture
def gen():
    yield iter([1, 2, 3, 4])


def test_head_correct(gen):
    # type: () -> None
    "Should return the first element of the iterator"
    assert P.head(gen) == 1


def test_tail_correct(gen):
    # type: () -> None
    "Should return the last"
    assert list(P.tail(gen)) == [2, 3, 4]


def test_tail_no_tail():
    # type: () -> None
    "Should not iterate on tail of only 1 element"
    n = 0
    for tailing in P.tail(iter([1])):
        n += 1
    assert n == 0


def test_pipe0():
    # type: () -> None
    "Should "
    afn = lambda x: x + 1
    bfn = lambda x: x + 2
    assert P.pipe(10, afn, bfn) == 13


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