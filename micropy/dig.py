# -*- coding: utf-8 -*-
# yapf

from . import lang
import funcy
import fnmatch
from dataclasses import dataclass
from functools import singledispatch

import pysistence


@dataclass
class Attr:
    infer_types = {}
    PrimType = lang.Undefined
    __bind__ = []

    @staticmethod
    def split(params):
        # type: (*Any) -> Tuple[str, Any]
        "Does split"
        name, value = '<anon:??>', None
        arity = len(params)
        if arity == 1:
            value, = params
            name = '<anon:{}>'.format(lang.typename(value))
        elif arity == 2:
            name, value = params
        else:
            raise ValueError('Incorrect arity')
        return name, value

    @classmethod
    def create(cls, *params):

        name, value = Attr.split(params)

        obj = cls.__new__(cls, value)
        obj.name = name

        @singledispatch
        def eq(other):
            raise NotImplementedError("Attr: eq not implemented for {}".format(
                type(other)))

        @eq.register(Attr)
        def _(other):
            # type: (other) -> None
            "Does _"
            return other.name == obj.name and other == obj

        @eq.register(cls.PrimType)
        def _(other):
            # type: (other) -> None
            "Does _"
            return other == obj.raw_value

        obj.eq = eq

        lang.bind_methods(cls, obj)

        return obj

    def __init__(self, name, value):
        self.name = name

    @staticmethod
    def isa(other):
        return isinstance(other, Attr.__class__)

    def sibling(self, other):
        return isinstance(other.__class__, Attr.__class__)

    def eq(self, other):
        return self.eq(self, other)

    @classmethod
    def infer(cls, *params):
        name, value = Attr.split(params)
        PrimType = Attr.infer_types[type(value)]
        return PrimType.create(name, value)

    @property
    def raw_value(self):
        # type: (self) -> None
        "Cast value to primitive type."

        # NB: Special case to avoid infinite recursion.
        if self.PrimType is str: return str.__str__(self)

        elif self.PrimType is lang.Undefined: return '????'

        else: return self.PrimType(self)

    @property
    def type_name(self):
        # type: (self) -> None
        "Return name of primitive type"

        # NB: Special case to avoid infinite recursion.
        if self.PrimType is str: return 'str'

        else: return self.PrimType.__name__

    def __str__(self):
        return "{}={}:{}".format(self.name, self.raw_value, self.type_name)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        # type: (self) -> None
        "Does __hash__"
        value = self.PrimType(self)
        return hashlib.sha1('{}:{}'.format(self.name, value)).hexdigest()

    def __eq__(self, other):
        if hasattr(other, 'name'):
            return other.name == self.name and other.raw_value == self.raw_value
        else:
            return other == self.raw_value


for name, PrimType in (('IntAttr', int),
                             ('FloatAttr', float),
                             ('TupleAttr', tuple),
                             ('ListAttr', list),
                             ('StrAttr', str)):  # yapf: disable
    AttrClass = lang.mkclass(name, (Attr, PrimType))
    AttrClass.PrimType = PrimType

    locals()[name] = AttrClass
    Attr.infer_types[PrimType] = AttrClass


class FoundAttrs(object):
    def __init__(self, initial):
        # type: (FoundAttrs, *Any) -> None
        self.found = pysistence.make_list(initial)

    def __getitem__(self, idx):
        # type: (self, int) -> Any
        "Subscript result"
        return tuple(self.found)[0][idx]

    def cons(self, next_item):
        # type: (self, el) -> None
        "Does cons"
        self.values = self.values.cons(next_item)
        return self

    def __iter__(self):
        return iter(self.found)

    def __len__(self):
        # type: (self) -> None
        "Does __len__"
        return len(self.found)

    def __repr__(self):
        return "/{}/".format(', '.join([str(el) for el in self.found.first]))


def xget(obj, idx):
    # type: (Any, Any) -> Optional[AttrResults, Attr]
    "Does foo"
    if lang.isprimitive(obj): return obj
    if callable(obj): return obj(idx)  # ???

    def attempt_many():
        # type: () -> None
        "Does attempt_many"
        vars_ = lang.pubvars(obj)
        attrs = fnmatch.filter(vars_, idx)
        attrified = [Attr.infer(attr, xget(obj, attr)) for attr in attrs]
        found = FoundAttrs(attrified)
        return found

    try:
        try:
            return obj[idx]
        except KeyError:
            return attempt_many()
        except IndexError:
            pass  # continue to next
    except TypeError:
        try:
            return getattr(obj, idx)
        except AttributeError:
            return attempt_many()


class AttrQuery(tuple):
    def __new__(cls, parts, *params, **opts):
        # type: (cls, name *params, **kwargs) -> None
        "Does __new__"
        pt, = lang.primbases(cls)
        instance = pt.__new__(cls, parts, *params, **opts)
        return instance

    @staticmethod
    def from_text(text):
        # type: (str) -> AttrQuery
        return AttrQuery(tuple(text.split('.')))


def dig(obj, path):
    # type: (Any, Tuple[Any]) -> FoundAttrs
    "Recursive query for attributes from `obj`"
    val = xget(obj, path[0])
    if lang.isprimitive(val):
        return Attr.infer(val)
    elif Attr.isa(val):
        dig(val, path[1:])
    else:
        return dig(val, path[1:])


if __name__ == '__main__':

    @IntAttr.method
    def foo(self, bar):
        # type: (self, bar) -> None
        "Does foo"
        return self + bar

    attr = IntAttr.infer('foo', 1)

    print(attr)
    print(attr.foo(2))
