from . import pipelib as pipelib
from pysistence import Expando
from typing import Any, Callable, Generator, Iterable, List, Mapping, Optional, Tuple, Union

PRIMTYPES: Any
LISTLIKE: Any
textual: Any
numeric: Any
isint: Any
isdict: Any
isgen: Any

def unfold_gen(x: Generator[Any, None, None], cast: type=...) -> Iterable[Any]: ...
def typename(x: Any) -> str: ...

class XE(Expando):
    def __getitem__(self, attr: str) -> Any: ...
    def iteritems(self) -> Mapping[str, Any]: ...
    def get(self, name: Any, default: Optional[Any] = ...): ...

def pubvars(obj: Any) -> Iterable: ...
def isprimitive(obj: Any): ...
def isprim_type(type_: Any): ...
def tolerant_or_original(Exc: Any, fn: Any): ...
def coerce_or_same(T: Any) -> str: ...

maybe_int: Any

def methdispatch(func: Any): ...

class Undefined: ...

def primbases(cls): ...
def bind_methods(Base: Any, instance: Any): ...
__classmethod__ = classmethod
__staticmethod__ = staticmethod

class Base:
    __bind__: List[Tuple[Callable, Any]] = ...
    def __init__(self, *params: Any, **opts: Any) -> None: ...
    def classmethod(cls, fn: Any): ...
    def staticmethod(fn: Callable) -> Callable: ...
    def method(Subclass: Any, fn: Callable) -> Callable: ...

def mkclass(name: str, bases: Tuple=..., **clsattrs: Any) -> Any: ...
def arity(fn: Callable) -> int: ...

always_tup: Any

class Piping(pipelib.BasePiping):
    class Fresh: ...
    class Executed: ...
    format: Any = ...
    kind: Any = ...
    seed: Any = ...
    def __init__(self, seed: Union[tuple, Any]=..., kind: Callable=..., format: Callable[[Any, None, None], Any]=...) -> Any: ...
    cursor: Any = ...
    ops: Any = ...
    results: Any = ...
    last_result: Any = ...
    def reset(self) -> None: ...
    def sum(self) -> None: ...
    @property
    def now(self): ...
    def fncompose(self, stepf: Callable[[Any, None, None], Any], x: Any=...) -> Piping: ...
    def queue(self, stepf: Callable[[Any, None, None], Any], *x: Any) -> Piping: ...
    def run(self, seed: Any, *x: Any) -> Any: ...
    @property
    def state(self): ...
    def calc_fmt_param(self, kind: Any, res: Any, params: Any, case: Any): ...
    def __call__(self, *params: Any) -> Any: ...

class ComposePiping(Piping):
    def __rshift__(self, stepf: Callable[[Any, None, None], Any]) -> None: ...

class CountPiping(Piping):
    def __add__(self, value: Any) -> Piping: ...
    def __sub__(self, value: Any) -> Piping: ...
    def __mul__(self, value: Any) -> Piping: ...
    def __div__(self, value: Any) -> Piping: ...

def PNot(value_or_stepf: Union[Callable, Any]) -> bool: ...
def P_has(idx: Union[str, Any]) -> Callable[[Any, None, None], Any]: ...

rcurry: Any

class LogicPiping(Piping):
    truthy: Any = ...
    conjunctions: int = ...
    def __init__(self, seed: Union[tuple, Any]=..., kind: Callable=..., format: Callable[[Any, None, None], Any]=...) -> Any: ...
    counter: Any = ...
    def logically(self, stepf: Any, conjunction: Any): ...
    def __call__(self, *params: Any) -> Any: ...
    def __eq__(self, value: Any) -> None: ...
    def __neg__(self, stepf: Any) -> None: ...
    def __ne__(self, value: Any) -> None: ...
    def __ge__(self, value: Any) -> None: ...
    def __gt__(self, value: Any) -> None: ...
    def __and__(self, stepf: Callable[[Any, None, None], Any]) -> Piping: ...
    def __floordiv__(self, stepf: Callable[[Any, None, None], Any]) -> Piping: ...
    def __or__(self, stepf: Callable[[Any, None, None], Any]) -> Piping: ...

class match(dict):
    def case(*params: Any) -> Callable: ...
    def __call__(self, *params: Any, **opts: Any) -> Union[Iterable[Any], Iterable]: ...
