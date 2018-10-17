from micropy import macro

def inline(x):
    100
    101


def test_body():
    # type: () -> None
    "Should poc"
    xx = macro.body(inline)
    assert tuple(exp.value.n for exp in xx) == (100, 101)
