import os
import unittest
from planning import search
from planning.PDDL import PDDL_Parser
from planning.relax import RelaxPrecondition, RelaxDeleteEffects


class TestRelax(unittest.TestCase):
    def setUp(self):
        domain_file = os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl')
        problem_file = os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl')
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        self.problem = search.Problem(parser)

    def test_apply_relax_precondition(self):
        relax = RelaxPrecondition()
        predicates = [('at', 'blank', '?s1')]
        relaxed_problem = relax.apply(self.problem, predicates)
        for action in self.problem.actions:
            for new_action in relaxed_problem.actions:
                self.assertTrue(new_action.positive_preconditions.issubset(action.positive_preconditions))
                if len(action.positive_preconditions) > 0:
                    self.assertTrue(len(new_action.positive_preconditions) < len(action.positive_preconditions))
                self.assertTrue(new_action.negative_preconditions.issubset(action.negative_preconditions))
                if len(action.negative_preconditions) > 0:
                    self.assertTrue(len(new_action.negative_preconditions) < len(action.negative_preconditions))

    def test_parameterize_relax_precondition(self):
        relax = RelaxPrecondition()
        for relaxed_problem in relax.parameterize(self.problem):
            for action in self.problem.actions:
                for new_action in relaxed_problem.actions:
                    self.assertTrue(new_action.positive_preconditions.issubset(action.positive_preconditions))
                    if len(action.positive_preconditions) > 0:
                        self.assertTrue(len(new_action.positive_preconditions) < len(action.positive_preconditions))
                    self.assertTrue(new_action.negative_preconditions.issubset(action.negative_preconditions))
                    if len(action.negative_preconditions) > 0:
                        self.assertTrue(len(new_action.negative_preconditions) < len(action.negative_preconditions))

    def test_apply_relax_delete_effects(self):
        relax = RelaxDeleteEffects()
        relaxed_problem = relax.apply(self.problem)
        for new_action in relaxed_problem.actions:
            self.assertTrue(new_action.del_effects == [])
