import pytest

import primitives as P


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
