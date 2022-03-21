import unittest
from planning.util import reduced_powerset, frozenset_of_tuples


class TestUtil(unittest.TestCase):
    def test_reduced_powerset(self):
        output = reduced_powerset([1, 2, 3])
        self.assertTrue(output == frozenset_of_tuples([[1], [2], [3], [1, 2], [1, 3], [2, 3]]))
        output = reduced_powerset([])
        self.assertTrue(output == frozenset())

