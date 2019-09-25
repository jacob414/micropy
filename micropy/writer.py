import types
import inspect


class BPAttr(object):
    def __init__(self, bp, name):
        self.bp = bp
        self.name = name

    def __getitem__(self, xx):
        # type: () -> None
        "Does BPAttr __getitem__"
        import ipdb
        ipdb.set_trace()

    def __call__(self, *args, **kw):
        # type: (self, *args, **kw) -> None
        "Does __call__"

        def create_function(name, args, kw):
            def y():
                pass

            y_code = y.__code__
            y_code = types.CodeType(
                len(args), len(kw), y_code.co_nlocals, y_code.co_stacksize,
                y_code.co_flags, y_code.co_code, y_code.co_consts,
                y_code.co_names, y_code.co_varnames, y_code.co_filename, name,
                y_code.co_firstlineno, y_code.co_lnotab)
            return types.FunctionType(y_code, globals(), name)

        fn = create_function(self.name, args, kw)
        setattr(self.bp, self.name, fn)


class Blueprint(object):
    def __init__(self):
        pass

    def __getattr__(self, name):
        # type: (self, name) -> None
        "Does __getattr__"
        if name not in dir(self):
            bpattr = BPAttr(self, name)
            setattr(self, name, bpattr)
            return bpattr
