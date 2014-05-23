from collections import namedtuple as _namedtuple
class BadImplementationError(Exception):
    pass

# Types
Trust = _namedtuple('Trust', ['truster', 'trusted'])
Predicate = _namedtuple('Predicate', ['predicate', 'true'])
Rule = _namedtuple('Rule', ['predicates', 'conclusions'])
Belief = _namedtuple('Belief', ['agent', 'predicate', 'level'])
Argument = _namedtuple('Argument', ['arg', 'belief'])
Labelling = _namedtuple('Labelling', ['inside', 'outside', 'undecided'])
Attack = _namedtuple('Attack', ['attacker', 'attacked'])

