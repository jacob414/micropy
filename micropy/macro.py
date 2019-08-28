import functools
import funcy
import patterns
import ast
import astor
import contextlib
from . import lang

noop = lambda *a, **kw: 0


@contextlib.contextmanager
def noop(*args, **kwargs):
    # type: (fn) -> None
    "Does noop"
    yield


def eval_(tree, name='expanded'):
    code = compile(tree, 'name', 'single')
    local = {}
    eval(code, globals(), local)
    return (v for v in local.values())


fake = block = type('Fake', (object, ), {
    'repeat': noop,
    'if_': noop,
    'inline': noop
})


def macro(fn):
    # type: (fn) -> None
    "Does macro"
    fn.body = lang.body(fn)

    # https://stackoverflow.com/a/16919884/288672

    def fixall(tree):
        ast.fix_missing_locations(tree)
        body = getattr(tree, 'body', None)
        if body:
            for node in body:
                fixall(node)
            else:
                ast.fix_missing_locations(body[0])

        return tree

    def transform(*args, **kwargs):
        # type: () -> None
        "An unmodified call"
        fn.__globals__['block'] = fake

        # Iterate nodes
        # if if_, rewrite as plain if
        def tfnode(node):
            # type: (node) -> None
            "Re-write"
            if type(node) is ast.With:
                witem, = node.items
                item, = node.items
                item.context_expr.func.attr
                if item.context_expr.func.attr == 'if_':
                    # Replace block.if_ w ast.If
                    with_args = item.context_expr.args
                    print('do if, args = {}'.format(with_args))
                    top = fixall(node)
                    return ast.fix_missing_locations(
                        ast.If(witem.context_expr.args,
                               ast.fix_missing_locations(top), None))

            return node

        newitems = funcy.walk(tfnode, fn.body)
        # XXX array of AST to ast object ??
        inter = ast.fix_missing_locations(ast.Interactive(body=newitems))  # ""
        inter.lineno = 1

        return eval_(inter)

    fn.macrofied = fake

    def expand(*args, **kwargs):
        # type: (*args, **kwargs) -> None
        "Does expand"
        fn.__globals__['block'] = fake
        recompiled = transform(*args, **kwargs)
        # Iterate nodes, do thing w help of *args, **kwargs
        # Recompile to code
        # recompiled = eval(<code fr above>)
        return recompiled

    fn.macrofied.expand = expand

    return fn
