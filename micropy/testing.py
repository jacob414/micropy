# -*- coding: utf-8 -*-
# -*- yapf -*-

from hypothesis import strategies as st
from funcy import namespace
import pytest

x = st.deferred(lambda: st.booleans() | st.tuples(x, x))


class strategy(namespace):
    like = lambda x: st.from_type(type(x))
    mydicts = lambda: st.dictionaries(('a', 'b', 'c'), (1, 2, 3))


strat = strategy

strats = {float: st.floats, int: st.integers, dict: strat.mydicts}

class fixture(namespace):
    def params(namelist, *values):
        # type: (namelist, values) -> None
        "Does params"
        return pytest.mark.parametrize(namelist, values)
