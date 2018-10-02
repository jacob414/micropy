from micropy.macro import macro

def test_poc():
    # type: () -> None
    "Should poc"
    @macro
    def expanded(x):
        return 'x'
    assert expanded('y') == 'xy'


