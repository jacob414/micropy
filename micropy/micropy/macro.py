import functools
import funcy
import patterns
import astor

def body(obj):
    import ipdb; ipdb.set_trace()
    return funcy.walk(lambda x: x.body, patterns.get_ast(obj).body)[0]


