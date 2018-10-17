import functools
import funcy
import patterns

def body(obj):
    return funcy.walk(lambda x: x.body, patterns.get_ast(obj).body)[0]
