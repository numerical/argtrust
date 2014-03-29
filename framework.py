from unittest import TestCase

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

    def A_plus(self, A):
        """
        A+ = { B | A def B }
        Returns all arguments defeated by A
        """
        return set(map(lambda l: l[1], filter(lambda x: x[0] == A, self._df)))

    def A_minus(self, A):
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
        raise NotImplementedError("defended_by")

    def F(self, Args):
        """F: 2**Ar -> 2**Ar
        F(Args) = { A | A is defended by Args }
        """

class TestArgumentationFramework(TestCase):

    def setUp(self):
        # Empty
        self.fig0 = ArgumentationFramework( {}, {} )

        self.fig1 = ArgumentationFramework( {'A', 'B', 'C'},
                [('C', 'B'), ('B', 'A')])

        # Circular
        self.fig2 = ArgumentationFramework( {'A', 'B', 'C'},
                { ('A', 'B'), ('B', 'C'), ('C', 'A') })

        # Nixon diamond
        self.fig3 = ArgumentaitonFrameWork( {'A', 'B'},
                { ('A', 'B'), ('B', 'A') } )

        self.fig4 = ArgumentaitonFrameWork( {'A', 'B', 'C', 'D'},
                { ('A', 'B'), ('B', 'C'), ('C', 'B'), ('C', 'D') } )

        self.fig5 = ArgumentationFramework( {'A', 'B', 'C', 'D', 'E'},
                { ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'C'), ('D', 'E')})

        self.fig6 = ArgumentationFramework( {'A', 'B', 'C', 'D'},
                { ('A', 'A'), ('A', 'C'), ('B', 'C'), ('C', 'D') })

