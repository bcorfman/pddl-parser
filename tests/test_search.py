import copy
import os
import unittest
from planning import search
from planning.action import Action
from planning.PDDL import PDDL_Parser
from planning.planner import Planner, parse_args
from planning.util import Queue


class TestSearch(unittest.TestCase):
    def test_problem_relax_action_delete_effects(self):
        domain_file = os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl')
        problem_file = os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl')
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        problem = search.Problem(parser)
        heuristic_class = search.HEURISTIC_CLASS['no_delete_effects']
        heuristic = heuristic_class()
        for relaxed_problem in heuristic.configure(problem):
            relaxed_problem.groundify_actions()
            for act in relaxed_problem.ground_actions:
                self.assertTrue(act.del_effects == frozenset())

    def test_problem_relax_action_preconditions(self):
        domain_file = os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl')
        problem_file = os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl')
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        problem = search.Problem(parser)
        heuristic_class = search.HEURISTIC_CLASS['relaxed_preconds']
        heuristic = heuristic_class()
        for relaxed_problem in heuristic.configure(problem):
            relaxed_problem.groundify_actions()
            for action in problem.ground_actions:
                for new_action in relaxed_problem.ground_actions:
                    self.assertTrue(new_action.positive_preconditions.issubset(action.positive_preconditions))
                    self.assertTrue(len(new_action.positive_preconditions) < len(action.positive_preconditions))
                    self.assertTrue(new_action.negative_preconditions.issubset(action.negative_preconditions))
                    self.assertTrue(len(new_action.negative_preconditions) < len(action.negative_preconditions))

