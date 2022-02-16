import copy
import os
import unittest
from planning.action import Action
from planning.PDDL import PDDL_Parser
from planning.planner import Planner, parse_args
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

    def test_problem_relax_action_delete_effects(self):
        domain_file = os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl')
        problem_file = os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl')
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        problem = search.Problem(parser)
        for act in problem.ground_actions:
            relaxed_action = problem.generate_relaxed_action_without_delete_effects(act)
            self.assertTrue(relaxed_action.del_effects == [])

    def test_problem_relax_action_preconditions(self):
        domain_file = os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl')
        problem_file = os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl')
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        problem = search.Problem(parser)

        for action in problem.ground_actions:
            for new_action in problem.generate_relaxed_actions_with_fewer_preconditions(action):
                self.assertTrue(new_action.positive_preconditions.issubset(action.positive_preconditions))
                self.assertTrue(len(new_action.positive_preconditions) < len(action.positive_preconditions))
                self.assertTrue(new_action.negative_preconditions.issubset(action.negative_preconditions))
                self.assertTrue(len(new_action.negative_preconditions) < len(action.negative_preconditions))
