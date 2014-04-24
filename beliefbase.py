from . import Belief, Rule, Predicate
from .framework import ArgumentationFramework
from collections import namedtuple as _namedtuple


class BeliefBase:
    """A BeliefBase is a SocialNetwork and a set of beliefs and rules that
    agents in the social network believe in
    """

    def __init__(self, sn, beliefs):
        """Constructor, takes a socialnetwork and a set/list of beliefs"""
        assert all([type(x) is Belief for x in beliefs])
        self._sn = sn
        self._beliefs = beliefs


    def query(self, who, query):
        """Given an agent in the socialnetwork and a query (a predicate)
        returns an argumentation framework that 
