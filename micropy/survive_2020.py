# -*- coding: utf-8 -*-
# yapf

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

try:
    from importlib import reload
except ImportError:
    reload = reload

try:
    # Python 2
    from itertools import izip_longest as pairs
except ImportError:
    # Python 3+
    from itertools import zip_longest as pairs

try:
    basestring
except NameError:
    basestring = str

try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch

try:
    import inspect
    inspect.signature
except AttributeError:
    import funcsigs as inspect
