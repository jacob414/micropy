from itertools import islice


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

