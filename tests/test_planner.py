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
from planning import search


class Test_Planner(unittest.TestCase):

    # -----------------------------------------------
    # Test solve
    # -----------------------------------------------

    def test_solve_dinner(self):
        planner = Planner()
        self.assertEqual(planner.solve(os.path.join('examples', 'dinner', 'dinner.pddl'),
                                       os.path.join('examples', 'dinner', 'pb1.pddl'),
                                       search.Domain, search.Problem, search.breadth_first_search),
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
        self.assertEqual(parser.search_algo, 'search.bfs')
        self.assertEqual(parser.domain_class, 'search.Domain')
        self.assertEqual(parser.problem_class, 'search.Problem')


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    unittest.main()
