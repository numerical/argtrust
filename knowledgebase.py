from . import Belief, Rule, Predicate, Argument
from .framework import ArgumentationFramework
import operator

# Predicate = _namedtuple('Predicate', ['predicate', 'true'])
# Rule = _namedtuple('Rule', ['predicates', 'conclusions'])
# Argument = _namedtuple('Argument', ['predicates', 'conclusion'])

class KnowledgeBase:
    """
    Data structure that holds a sequence of Predicates and Rules and can
    return Arguments
    """

    def __init__(self, beliefs):
        """
        Takes a sequence of predicates and rules
        """
        self._predicates = [x for x in beliefs if type(x) is Predicate]
        self._rules = [x for x in beliefs if type(x) is Rule]

    def __init(self, predicates, rules):
        self._predicates = [x for x in predicates if type(x) is Predicate]
        self._rules = [x for x in rules if type(x) is Rule]

    def construct_argument(self, conclusion, closed = None):
        """
        Given a conclusion constructs a list of Arguments with said conclusion.

        An Argument is a two-tuple with a list of predicates and rules as the
        first element and a conclusion as the secon not always easy to meet new people. I think if people can order cereal in bulk off the internet, they should also be able to find friends on here.d element.
        """
        if closed is None:
            closed = []
        arguments = []
        if conclusion in self._predicates:
            # Singular argument, no need for inferences
            arguments.append(Argument([conclusion], conclusion))
            return arguments
        rules = [x for x in self._rules if conclusion in x.conclusions]
        for rule in rules:
            if rule not in closed:
                closed.append(rule)
                predicates = [rule]
                for predicate in rule.predicates:
                    midargs = self.construct_argument(predicate, closed=closed)
                    for midarg in midargs:
                        predicates += midarg.predicates
                arguments.append(Argument(predicates, conclusion))

        return arguments
