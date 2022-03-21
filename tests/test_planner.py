#!/usr/bin/env python
# Four spaces as indentation [no tabs]

# This file is part of PDDL Parser, available at <https://github.com/pucrs-automated-planning/pddl-parser>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import unittest
from planning.action import Action
from planning.planner import Planner, parse_args
from planning import heuristic, relax, search


class Test_Planner(unittest.TestCase):

    # -----------------------------------------------
    # Test solve
    # -----------------------------------------------

    def test_solve_dinner(self):
        planner = Planner()
        self.assertEqual(planner.solve(os.path.join('examples', 'dinner', 'dinner.pddl'),
                                       os.path.join('examples', 'dinner', 'pb1.pddl'),
                                       [], None, 'bfs', 60),
                         [
                             Action('cook', [], [['clean']], [], [['dinner']], []),
                             Action('wrap', [], [['quiet']], [], [['present']], []),
                             Action('carry', [], [['garbage']], [], [], [['garbage'], ['clean']])
                         ]
                         )

    def test_parser_default_args(self):
        parser = parse_args([os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl'),
                             os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl')])
        self.assertEqual(parser.domain_file, os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl'))
        self.assertEqual(parser.problem_file, os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl'))
        self.assertEqual(search.ALGORITHMS[parser.search_type], search.breadth_first_search)

    def test_parser_astar_args(self):
        args = parse_args([os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl'),
                           os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl'),
                           '-R=no_delete_effects', '-S=astar', '-H=max'])
        self.assertEqual(args.domain_file, os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl'))
        self.assertEqual(args.problem_file, os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl'))
        self.assertEqual(search.ALGORITHMS[args.search_type], search.astar_search)
        self.assertEqual(search.HEURISTIC_CLASS[args.heuristic_type], heuristic.h_max)
        self.assertEqual(search.RELAXING_TRANSFORMATIONS[args.transformations[0]], relax.RelaxDeleteEffects)

    def test_planner_setup_relaxed_problem(self):
        args = parse_args([os.path.join('examples', 'n_puzzle', 'n_puzzle.pddl'),
                           os.path.join('examples', 'n_puzzle', 'eight_puzzle_pb1.pddl'),
                           '-R=no_delete_effects', '-S=astar', '-H=max'])
        planner = Planner()
        parser = planner.parse(args.domain_file, args.problem_file)
        search_algo = search.ALGORITHMS[args.search_type]
        cost_estimate, _ = planner.solve_relaxed_problem(parser, search_algo, args.transformations, args.heuristic_type)
        self.assertEqual(cost_estimate, 21)


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    unittest.main()
