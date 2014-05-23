from collections import namedtuple as _namedtuple
from . import Trust
import pydot as _pydot

# Trust = _namedtuple('Trust', ['truster', 'trusted'])

class SocialNetwork:
    """
    A social network is a group of individuals, Ags, and the set of directed
    relations between individuals, trust, where each element of trust is a
    three-tuple consisting of truster and trustee in Ags, and a trust
    value between 0 and 1 where 0 is no trust and 1 is fully trust. Trust can
    be propogated from a in Ags to some z in Ags in many ways. The way trust
    propogates is through linking (i.e. transitivity) and composability
    (i.e. updating trust ratings based on two different links from a to z)

    Note: This object only holds one value of trust per trust relation so that
    the rules of transitivity and composability hold
    [J. Golbeck umi-umd-2244.pdf pg74].
    """

    def __init__(self, Ags, tau, transitive_operator=min, paths_operator=max):
        """Constructor
        Arguments:
        --> Ags: Iterator of agents
        --> tau: Set of trust in the form of 3-tuples consisting of truster,
                 trustee and trust value (0.0-1.0)
        """
        self._transitive_operator = transitive_operator
        self._paths_operator = paths_operator
        self._Ags = set(Ags)
        self._tau = {Trust(*x[:2]) for x in tau}
        self._tr  = dict()
        for rel in tau:
            if rel[:2] in self._tr:
                raise MalformedNetwork(
                        "Two values for the same relationship. %s -> %s" %
                        rel[:2])
            self._tr[rel[:2]] = rel[2]

    def __len__(self):
        return len(self._Ags)

    def __iter__(self):
        return iter(self._Ags)

    def find_paths(self, source, destination, closed=None):
        """Does a breadth first search to find all paths from source to
        destination
        """
        if closed is None:
            closed = set()
        closed.add(source)
        links = {x.trusted for x in self._tau
                if x.truster == source and x.trusted not in closed}
        if len(links) == 0: # base
            return []
        if destination in links: # base
            return [[Trust(source, destination)]]
        # recurse
        retval = []
        for link in links:
            linkpaths = self.find_paths(link, destination, closed)
            for path in linkpaths:
                path.insert(0, Trust(source, link))
            retval += linkpaths

        for path in retval:
            if None in path:
                retval.remove(path)
        if len(retval) == 0:
            return []
        return retval

    def trusts(self, truster, trustee):
        """Returns a scalar saying how much truster trusts trustee.
        uses transitive_operator to combine trusts in a path and paths_operator
        to combine trust paths"""
        assert truster in self._Ags
        assert trustee in self._Ags

        trust = 0 # MIN TRUST TODO make this a constant for other modes of trust
        paths = self.find_paths(truster, trustee)
        for path in paths:
            path_trust = 1.0 # MAX TRUST TODO same as MIN TRUST
            for link in path:
                path_trust = self._transitive_operator(path_trust, link)

            trust = self._paths_operator(trust, path_trust)

        return trust

    def agent_centric(self, agent):
        """Given an agent returns an agent centric graph.

        An agent centric graph is a sub graph that only
        includes agent as a root and any other agents that can be reached
        from the agent specified"""
        if agent not in self._Ags:
            raise ValueError("No such agent in social network")
        Ags = [x for x in self._Ags if self.find_path(x) != None]
        tau = [(x, self._tr[x]) for x in self._tau if x.truster in Ags and x.trusted in Ags]
        return SocialNetwork(Ags, tau)
