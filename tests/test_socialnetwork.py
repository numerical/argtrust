import unittest
from argtrust.socialnetwork import SocialNetwork

class TestSocialNetwork(unittest.TestCase):

    def setUp(self):
        """See Semantics_Overview.pdf for these figures"""
        agents = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        # Empty
        self.sn0 = SocialNetwork( {}, {} )

        # Two person unidrectional
        self.sn1 = SocialNetwork( agents[:2], {('A', 'B', 0.5)})

        self.sn2 = SocialNetwork( agents[:3], {('A', 'B', 0.5), ('A', 'C', 0.8)})
        self.sn3 = SocialNetwork( agents[:3], {('A', 'B', 0.5), ('B', 'C', 0.8)})
        self.sn4 = SocialNetwork( agents[:4], {('A', 'B', 0.5), ('A', 'C', 0.8), ('B', 'D', 0.4), ('C', 'D', 0.7)} )

        self.sn5 = SocialNetwork( agents, {('A', 'B', 1.0)})

    def test_trusts(self):
        self.assertEqual(self.sn1.trusts('A', 'B'), 0.5)
        self.assertEqual(self.sn3.trusts('A', 'C'), 0.5)
        self.assertEqual(self.sn4.trusts('A', 'D'), 0.7)

    def test_agent_centric(self):
        tmpsn = self.sn5.agent_centric('A')
        self.assertCountEqual(tmpsn._Ags, ['A', 'B'])

    def test_find_paths(self):
        self.assertEqual(len(self.sn4.find_paths('A', 'D')), 2)

if __name__ == "__main__":
    unittest.main()

