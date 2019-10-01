# -*- coding: utf-8 -*-
# yapf

from pprint import pformat
import json
import jsonpickle

from typing import Any


def expose(x: Any) -> str:
    # type: (x) -> None
    """Abuses modules `json` and `jsonpickle` to expose internals of
    (almost) any object

    """
    return json.loads(jsonpickle.dumps(x))


def look(x, shrink_right=' '):
    # type: (x) -> None
    "Does look"
    print(print(pformat(expose(x)).replace('    ', shrink_right)))
