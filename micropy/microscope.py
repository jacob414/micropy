# -*- coding: utf-8 -*-
# yapf

from pprint import pformat
import json
import jsonpickle  # type: ignore

from typing import Any


def expose(x: Any, shrink_right: int = 1) -> str:
    """Abuses modules `json` and `jsonpickle` to expose internals of
    (almost) any object.

    """
    return json.loads(jsonpickle.dumps(x))


def look(x: Any, shrink_right: int = 1) -> None:
    """Dumps any object to stdout using the technique in `expose()`.

    The parameter `shrink_right` is used to set narrowing of
    indentation. (Use `0` to turn off).

    """
    print(pformat(expose(x, shrink_right)).replace('    ', shrink_right * ' '))
