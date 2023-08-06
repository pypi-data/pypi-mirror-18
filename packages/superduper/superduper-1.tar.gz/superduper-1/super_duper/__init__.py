"""
    Don't take it seriously. It's just a joke.
    Remember that usage of hacks like this is a bad practice.
"""


def superduper(Klass, instance):
    return super(Klass.__base__, instance)