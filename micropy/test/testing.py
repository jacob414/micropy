# yapf

from hypothesis.strategies import *
import string

from micropy import lang

from micropy.survive_2020 import inspect

hairy_strategy = recursive(
    none() | booleans() | floats() | text(alphabet=string.hexdigits),
    (lambda children: lists(children, 1) | dictionaries(
        text(alphabet=string.hexdigits), children, min_size=1)))

from altered import E


def hairy_ob():
    # type: () -> Any
    """Returns a Hypothesis-generated example of `hairy_strategy`. Good
    for interactive torture of functions.

    """
    return hairy_strategy.example()


def flexilize(Rigid):
    # type: (Any) -> Any
    """Takes a class and creates a version of it that will ignore any
    extra positional parameters passed to it's constructor.

    >> class Rigid(object):
    >>     def __init__(self, a, b, x=1):
    >>         pass

    >> Flexi = flexilize(Rigid)

    >> Flexi(1, 2, (3, )) # no exception
    >> Flexi(1, 2, 3, 4, x=18) # no exceptiopn

    """
    sig = inspect.signature(Rigid.__init__)
    actual_positional_params = [par for par in sig.parameters if par != 'self']

    def FlexibleObjectFactory(*positional, **by_keyword):
        # type: (Rigid) -> None
        "Instantiate with any possible parameters"
        return Rigid(*positional[:len(actual_positional_params) - 1],
                     **by_keyword)

    return FlexibleObjectFactory
