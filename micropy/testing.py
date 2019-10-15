# -*- coding: utf-8 -*-
# yapf

from hypothesis import strategies as st
from hypothesis.searchstrategy.lazy import SearchStrategy
from funcy import namespace
import pytest

from typing import Any


class strategy(namespace):  # pragma: nocov
    def like(x: Any) -> SearchStrategy:
        "Convenience method to find a Hypothesis Strategy for an object."
        return st.from_type(type(x))

    def mydicts() -> SearchStrategy:
        "Does mydicts"
        return st.dictionaries(('a', 'b', 'c'), (1, 2, 3))


strat = strategy

strats = {float: st.floats, int: st.integers, dict: strat.mydicts}


class fixture(namespace):
    def params(namelist: str, *values: Any) -> Any:
        "Does params"
        return pytest.mark.parametrize(namelist, values)
