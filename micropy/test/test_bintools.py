from micropy import bintools


def test_binstr():
    # type: () -> None
    "Should convert an int to a string in conventient human-readable form"
    assert bintools.binstr(0b101) == '00000101'


def test_nv():
    # type: () -> None
    "Should be a convenient application of binstr()"
    assert bintools.nv(0b101) == '00000101'


def test_snv():
    # type: () -> None
    "Should convert an int to a plesantly spaced string"
    assert bintools.snv(0b101) == '0  0  0  0  0  1  0  1'


def test_hexdump():
    # type: () -> None
    "Should print a pleasantly spaced hex dump of a string"
    assert bintools.hexdump('\x01\x02\x03\x3a') == '01 02 03 3a'
