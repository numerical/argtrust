import unittest
from argtrust.framework import ArgumentationFramework

class TestArgumentationFramework(unittest.TestCase):

    def setUp(self):
        """See Semantics_Overview.pdf for these figures"""
        # Empty
        self.fig0 = ArgumentationFramework( {}, {} )

        self.fig1 = ArgumentationFramework( {'A', 'B', 'C'},
                [('C', 'B'), ('B', 'A')])

        # Circular
        self.fig2 = ArgumentationFramework( {'A', 'B', 'C'},
                { ('A', 'B'), ('B', 'C'), ('C', 'A') })

        # Nixon diamond
        self.fig3 = ArgumentationFramework( {'A', 'B'},
                { ('A', 'B'), ('B', 'A') } )

        self.fig4 = ArgumentationFramework( {'A', 'B', 'C', 'D'},
                { ('A', 'B'), ('B', 'C'), ('C', 'B'), ('C', 'D') } )

        self.fig5 = ArgumentationFramework( {'A', 'B', 'C', 'D', 'E'},
                { ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'C'), ('D', 'E')})

        self.fig6 = ArgumentationFramework( {'A', 'B', 'C', 'D'},
                { ('A', 'A'), ('A', 'C'), ('B', 'C'), ('C', 'D') })

    def test_minus(self):
        self.assertEqual(self.fig1.minus('A'), {'B'})
        self.assertEqual(self.fig1.minus('B'), {'C'})
        self.assertEqual(self.fig1.minus('C'), set())

    def test_plus(self):
        self.assertEqual(self.fig1.plus('A'), set())
        self.assertEqual(self.fig1.plus('B'), {'A'})
        self.assertEqual(self.fig1.plus('C'), {'B'})

    def test_args_plus(self):
        self.assertEqual(self.fig1.args_plus({'A', 'B'}), {'A'})
        self.assertEqual(self.fig2.args_plus({'A', 'B'}), {'B', 'C'})
        self.assertEqual(self.fig3.args_plus({'A', 'B'}), {'A', 'B'})
        self.assertEqual(self.fig4.args_plus({'B', 'C'}), {'B', 'C', 'D'})

    def test_args_minus(self):
        self.assertEqual(self.fig1.args_minus({'B'}), {'C'})
        self.assertEqual(self.fig3.args_minus({'A', 'B'}), {'A', 'B'})
        self.assertEqual(self.fig4.args_minus({'A', 'D', 'B'}), {'A', 'C'})
        self.assertEqual(self.fig5.args_minus({'C', 'D'}), {'C', 'D', 'B'})
        self.assertEqual(self.fig6.args_minus({'A', 'B', 'C', 'D'}), {'A', 'C', 'B'})


    def test_defends(self):
        pass

    def test_F(self):
        pass


if __name__ == "__main__":
    unittest.main()

