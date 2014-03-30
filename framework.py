from itertools import combinations

class ArgumentationFramework:
    """
    If one abstracts from the internal structure of an argument, as well as
    from the reasons why they defeat each other, what is left is called an
    argumentation framework: An argumentation framework simply consists of a
    set of (abstract) arguments and a binary defeat relation between these
    arguments.
    -- Caminada, A Gentle Introduction to Argumentation Semantics, Summer 2008
    """

    def __init__(self, Ar, df):
        """
        Takes the sets Ar and ``def''
        Ar is a set of arguments
        ``def'' is a set of two-tuples in the form (attacker, attackee)
        """
        self._Ar = set(Ar)
        self._df = set(df)

    def __len__(self):
        """Return the amount of arguments for len(ArgumentationFramework)"""
        return len(self._Ar)

    def make_generator(self, up=True):
        if up:
            for i in range(len(self._Ar)+1):
                for j in combinations(self._Ar, i):
                    yield set(j)
        else:
            for i in range(len(self._Ar), -1, -1): # iterate from top to bottom
                for j in combinations(self._Ar, i):
                    yield set(j)

    def plus(self, A):
        """
        A+ = { B | A def B }
        Returns all arguments defeated by A
        """
        assert A in self._Ar
        return set(map(lambda l: l[1], filter(lambda x: x[0] == A, self._df)))

    def minus(self, A):
        """
        A- = { B | B def A }
        Returns all arguments that defeat A
        """
        assert A in self._Ar
        return set(map(lambda l: l[0], filter(lambda x: x[1] == A, self._df)))

    def args_plus(self, Args):
        """
        Args+ = { B | A def B for some A in Args }
        Returns all arguments that are defeated by an argument in Args
        """
        assert Args.issubset(self._Ar)
        return set(map(lambda x: x[1],
            filter(lambda l: l[0] in Args, self._df)))

    def args_minus(self, Args):
        """
        Args- = { B | B def A for some A in Args }
        Returns all arguments that defeat an argument in Args
        """
        assert Args.issubset(self._Ar)
        return set(map(lambda x: x[0],
            filter(lambda l: l[1] in Args, self._df)))

    def conflict_free(self, Args):
        """
        Args is said to be conflict-free iff Args intersect Args+ is empty
        """
        assert Args.issubset(self._Ar)
        return Args.intersection(self.args_plus(Args)).issubset(set())

    def defends(self, Args, B):
        """
        Args is said to defend B iff B- is in Args+
        Returns True if Args defends B, False otherwise
        """
        assert Args.issubset(self._Ar)
        assert B in self._Ar
        return self.minus(B).issubset(self.args_plus(Args))

    def F(self, Args):
        """F: 2**Ar -> 2**Ar
        F(Args) = { A | A is defended by Args }
        """
        assert Args.issubset(self._Ar)
        # Filters out all arguments that defended by Args
        return filter(lambda x: self.defends(Args, x), self._Ar)

    def admissible(self, Args):
        """
        Args is said to be admissible iff Args is conflict-free
        and args is a subset of F(Args)
        """
        assert Args.issubset(self._Ar)
        return self.conflict_free(Args) and Args.issubset(self.F(Args))

    def grounded_extension(self):
        """
        Minimal fixpoint of F
        """
        raise NotImplementedError("grounded")

    def preferred_extension(self):
        """
        Maximal admissible set
        """
        raise NotImplementedError("preferred")

    def semistable_extension(self):
        """
        Admissible set with maximum Args union Args+
        complete extension with max Args union Args+
        """
        raise NotImplementedError("semistable")

    def stable_extension(self):
        """
        Args defeating exactly Ar\Args
        conflict-free Args defeating Ar\Args
        admissible set Args defeating Ar\Args
        complete extension Args defeating Ar\Args
        preferred extension Args defeating Ar\Args
        semi-stable extension Args defeating Ar\Args
        """
        raise NotImplementedError("stable")




