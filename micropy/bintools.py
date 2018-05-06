def binstr(value, width=8):
    # type: (int, int) -> str
    prefixd = width + 3
    fmt = "#{}b".format(prefixd)
    return format(value, fmt).strip().replace('0b', '').zfill(width)


def snv(value, width=8):
    # type: (int, int) -> str
    return '  '.join(
        idx % 2 == 2 and ch + ' ' or ch for idx, ch in enumerate(binstr(value))
    )


def hexdump(bytes_):
    # type: (bytes) -> str
    return ' '.join(format(ord(x), 'x').zfill(2) for x in bytes_)
