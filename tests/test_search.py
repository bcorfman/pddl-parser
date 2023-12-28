import copy
import os
import unittest
from planning.PDDL import PDDL_Parser
from planning.relax import RelaxPrecondition, RelaxDeleteEffects
from planning import search


class TestSearch(unittest.TestCase):
    def test_problem_copy(self):
        domain_file = os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl')
        problem_file = os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl')
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        problem = search.Problem(parser)
        problem2 = copy.copy(problem)
        problem2.name = 'junk'
        problem2.state = frozenset(['hello'])
        problem2.positive_goals = frozenset(['positive'])
        problem2.negative_goals = frozenset(['negative'])
        problem2.cost = 99999
        problem2.requirements = ['stuff']
        problem2.types = {'type1'}
        problem2.objects = {'object'}
        problem2.predicates = {'predicate'}
        problem2.ground_actions = ['ground_action']
        self.assertTrue(problem.name != problem2.name)
        self.assertTrue(problem.state != problem2.state)
        self.assertTrue(problem.positive_goals != problem2.positive_goals)
        self.assertTrue(problem.negative_goals != problem2.negative_goals)
        self.assertTrue(problem.cost != problem2.cost)
        self.assertTrue(problem.requirements != problem2.requirements)
        self.assertTrue(problem.types != problem2.types)
        self.assertTrue(problem.objects != problem2.objects)
        self.assertTrue(problem.predicates != problem2.predicates)
        self.assertTrue(problem.ground_actions != problem2.ground_actions)

