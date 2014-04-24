from collections import namedtuple as _namedtuple
class BadImplementationError(Exception):
    pass

Predicate = _namedtuple('Predicate', ['predicate', 'true'])
Rule = _namedtuple('Rule', ['predicates', 'conclusions'])
Belief = _namedtuple('Belief', ['agent', 'predicate', 'level'])


