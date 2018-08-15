import inspect
from .primitives import XE
from funcy import merge

def full():
    # all_ = XE(**dict(globals(), **locals()))
    all_ = XE()
    try:
        frame = inspect.currentframe()
        while frame.f_back:
            frame = frame.f_back
            visible = merge(frame.f_globals, frame.f_locals)
            print('up')
            all_ = all_.using(**visible)
        return all_
    finally:
        del frame

def name():
    name_foo, name_bar = 'name_foo', 'name_bar'
    return full()

from pprint import pprint


_st = name()
# pprint(_st)

