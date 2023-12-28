import unittest
from planning.util import reduced_powerset, frozenset_of_tuples


class TestUtil(unittest.TestCase):
    def test_reduced_powerset_numbers(self):
        output = reduced_powerset([1, 2, 3])
        self.assertTrue(output == frozenset_of_tuples([[1], [2], [3], [1, 2], [1, 3], [2, 3]]))
        output = reduced_powerset([])
        self.assertTrue(output == frozenset())

    def test_reduced_powerset_predicates(self):
        predicates = reduced_powerset([['adjacent', '?s1', '?s2'], ['at', 'blank', '?s1'], ['at', '?t', '?s2']])
        self.assertTrue(predicates == frozenset_of_tuples([['adjacent', '?s1', '?s2'], ['at', 'blank', '?s1'],
                                                           ['at', '?t', '?s2'],
                                                           [['adjacent', '?s1', '?s2'], ['at', 'blank', '?s1']],
                                                           [['adjacent', '?s1', '?s2'], ['at', '?t', '?s2']],
                                                           [['at', 'blank', '?s1'], ['at', '?t', '?s2']]]))
