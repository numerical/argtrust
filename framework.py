
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

    def plus(self, A):
        """
        A+ = { B | A def B }
        Returns all arguments defeated by A
        """
        return set(map(lambda l: l[1], filter(lambda x: x[0] == A, self._df)))

    def minus(self, A):
        """
        A- = { B | B def A }
        Returns all arguments that defeat A
        """
        return set(map(lambda l: l[0], filter(lambda x: x[1] == A, self._df)))

    def args_plus(self, Args):
        """
        Args+ = { B | A def B for some A in Args }
        Returns all arguments that are defeated by an argument in Args
        """
        return set(map(lambda x: x[1],
            filter(lambda l: l[0] in Args, self._df)))

    def args_minus(self, Args):
        """
        Args- = { B | B def A for some A in Args }
        Returns all arguments that defeat an argument in Args
        """
        return set(map(lambda x: x[0],
            filter(lambda l: l[1] in Args, self._df)))

    def defends(self, Args, B):
        """
        Args is said to defend B iff B- is in Args+
        Returns True if Args defends B, False otherwise
        """
        return self.minus(B).issubset(self.args_plus(Args))

    def F(self, Args):
        """F: 2**Ar -> 2**Ar
        F(Args) = { A | A is defended by Args }
        """
        # Filters out all arguments that defended by Args
        return filter(lambda x: self.defends(Args, x), self._Ar)

    def grounded_extension(self):
        raise NotImplementedError("grounded")

    def stable_extension(self):
        raise NotImplementedError("stable")

    def semistable_extension(self):
        raise NotImplementedError("semistable")

    def preferred_extension(self):
        raise NotImplementedError("preferred")


