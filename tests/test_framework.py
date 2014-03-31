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

    def test_make_generator(self):
        generator = self.fig6.make_generator()
        count = 0
        for s in generator:
            count += 1
            self.assertTrue(s.issubset(self.fig6._Ar))
        self.assertEqual(count, 2**len(self.fig6))

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

    def test_conflict_free(self):
        self.assertTrue(self.fig0.conflict_free(set()))
        self.assertTrue(self.fig1.conflict_free({'A','C'}))
        self.assertTrue(self.fig1.conflict_free({'A'}))
        self.assertTrue(self.fig3.conflict_free({'A'}))
        self.assertTrue(self.fig3.conflict_free({'B'}))
        self.assertTrue(self.fig5.conflict_free({'A', 'C', 'E'}))

        self.assertFalse(self.fig1.conflict_free({'B', 'A'}))
        self.assertFalse(self.fig1.conflict_free({'A', 'B', 'C'}))
        self.assertFalse(self.fig2.conflict_free({'C', 'B'}))
        self.assertFalse(self.fig6.conflict_free({'A', 'A'}))

    def test_defends(self):
        self.assertTrue(self.fig1.defends({'C'}, 'A'))
        self.assertTrue(self.fig2.defends({'C'}, 'B'))
        self.assertTrue(self.fig4.defends({'A', 'C', 'B'}, 'D'))
        self.assertTrue(self.fig6.defends({'A', 'B'}, 'D'))

        self.assertFalse(self.fig1.defends({'B'}, 'A'))
        self.assertFalse(self.fig4.defends({'C', 'D'}, 'B'))
        self.assertFalse(self.fig6.defends({'A'}, 'C'))

    def test_F(self):
        self.assertEqual(self.fig1.F({'C', 'A'}), {'A', 'C'})
        self.assertEqual(self.fig1.F({'C'}), {'A', 'C'})
        self.assertEqual(self.fig2.F({'A'}), {'C'})
        self.assertEqual(self.fig3.F({'A'}), {'A'})
        self.assertEqual(self.fig3.F({'B'}), {'B'})
        self.assertEqual(self.fig4.F({'B'}), {'A', 'D'})
        self.assertEqual(self.fig5.F({'C', 'D'}), {'A', 'E', 'D'})

    def test_admissible(self):
        self.assertTrue(self.fig1.admissible({'C'}))
        self.assertTrue(self.fig1.admissible({'A', 'C'}))
        self.assertTrue(self.fig3.admissible({'B'}))
        self.assertTrue(self.fig3.admissible({'A'}))
        self.assertTrue(self.fig4.admissible({'A', 'C'}))

        self.assertFalse(self.fig2.admissible({'A'}))
        self.assertFalse(self.fig2.admissible({'C'}))
        self.assertFalse(self.fig6.admissible({'A', 'B', 'D'}))

if __name__ == "__main__":
    unittest.main()

