import functools
import funcy

def macro(fn):
    def deco(*args, **kw):
        return fn(*args, **kw)+args[0]
    return deco
