from itertools import combinations
from . import BadImplementationError
try:
    import pydot
except ImportError:
    print ("Unable to import pydot. pydot support not enabled")

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
        for attack in self._df:
            assert attack[0] in self._Ar
            assert attack[1] in self._Ar

    def __len__(self):
        """Return the amount of arguments for len(ArgumentationFramework)"""
        return len(self._Ar)

    def make_generator(self, up=True):
        """Returns a generator that cycles through every combination of Ar
        if up is True starts generating from the empty set to Ar, otherwise
        starts generating from Ar to the empty set
        """
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
        return {l[1] for l in filter(lambda x: x[0] == A, self._df)}

    def minus(self, A):
        """
        A- = { B | B def A }
        Returns all arguments that defeat A
        """
        assert A in self._Ar
        return {l[0] for l in filter(lambda x: x[1] == A, self._df)}

    def args_plus(self, Args):
        """
        Args+ = { B | A def B for some A in Args }
        Returns all arguments that are defeated by an argument in Args
        """
        assert Args.issubset(self._Ar)
        return {x[1] for x in filter(lambda l: l[0] in Args, self._df)}

    def args_minus(self, Args):
        """
        Args- = { B | B def A for some A in Args }
        Returns all arguments that defeat an argument in Args
        """
        assert Args.issubset(self._Ar)
        return {x[0] for x in filter(lambda l: l[1] in Args, self._df)}

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
        return set(filter(lambda x: self.defends(Args, x), self._Ar))

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
        There is guaranteed to be a smallest fixpoint by the Knaster-Tarski
        theorem. Function will raise BadImplementationError
        (I scold myself daily) if the minimal fixpoint was not found
        """
        generator = self.make_generator()
        for Args in generator:
            if Args == self.F(Args):
                return Args
        raise BadImplementationError("Minimal fixpoint exists but wasn't found")

    def preferred_extension(self):
        """
        Maximal admissible set
        Returns a set of frozensets (this is a python requirement since sets
        are not hashable)
        """
        max_admissible = 0
        returnable = set()
        generator = self.make_generator(up=False)
        while True:
            try:
                s = next(generator)
                if len(s) < max_admissible:
                    return returnable
                if self.admissible(s):
                    max_admissible = len(s)
                    returnable.add(frozenset(s))
            except StopIteration: # No more sets to check
                break
        return returnable

    def semistable_extension(self):
        """
        Admissible set with maximum Args union Args+
        complete extension with max Args union Args+
        """
        maximized = -1
        returnable = set()
        preferred = self.preferred_extension()
        for Args in preferred:
            a_size = len(Args.union(self.args_plus(Args)))
            if a_size > maximized:
                maximized = a_size
                returnable = {frozenset(Args)}
            elif a_size == maximized:
                returnable.add(frozenset(Args))
        return returnable

    def stable_extension(self):
        """
        Args defeating exactly Ar\Args
        Args is a stable extension iff Args+ = Ar \ Args
        """
        preferred = self.semistable_extension()
        returnable = set()
        for Args in preferred:
            plus = self.args_plus(Args)
            if plus == self._Ar.difference(Args):
                returnable.add(Args)

        return returnable

    def print_dot_graph(self, path, Args=[]):
        """Prints the framework to a file.
        Writes using extension for type of file to write.
        If extension isn't known defaults to pdf
        If Args is given marks all elements of Args with a doublecircle

        Possible formats:
        jpg, jpeg, png, pdf, ps
        """

        try:
            graph = pydot.Dot()
        except NameError:
            print("Not able to import pydot. This functionality will not work.")
            return

        for arg in self._Ar:
            graph.add_node(pydot.Node(str(arg), shape='circle'))

        for attack in self._df:
            graph.add_edge(pydot.Edge(str(attack[0]), str(attack[1])))

        for arg in Args:
            graph.get_node(str(arg)).pop().set_shape('doublecircle')


        func = graph.write_pdf
        if path.endswith('.jpg'):
            func = graph.write_jpg
        elif path.endswith('.jpeg'):
            func = graph.write_jpeg
        elif path.endswith('.png'):
            func = graph.write_png
        elif path.endswith('.pdf'):
            func = graph.write_pdf
        elif path.endswith('.ps'):
            func = graph.write_ps
        else:
            path = path + ".png"

        if not func(path):
            print("Could not print")

        return
