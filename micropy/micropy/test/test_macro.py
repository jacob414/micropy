# yapf
import pytest
from micropy.macro import macro, block


def inline(x):
    100
    101


@pytest.fixture
def macro_():
    # type: () -> None
    "Does macro_wishlisted"

    expr = lambda x: x + 1

    @macro
    def macrofied(foo, bar):
        # type: (foo, bar) -> None
        "Does macrofied"
        ret = 1
        with block.repeat(bar) as idx:
            ret += 1

        with block.if_(foo == 'cond'):
            ret += 1

        with block.inline():
            res = expr(ret)

        return ret

    yield macrofied


def test_macro_call_no_repeat_no_if_no_inline(macro_):
    # type: () -> None
    "Should expand macro"
    # call results in exactly 1 repeat, if_ supressed, .inline() not supressed.
    assert macro_(1, 2) == 3


@pytest.mark.skip
def test_macro_does_repeat_only(macro_):
    # type: () -> None
    "Should expand macro"
    # repeat 1 time, inline expr
    assert macro_.macrofied.expand(1, 2) == 4
