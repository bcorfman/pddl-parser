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
import argparse
import math
import sys
import time
from planning.PDDL import PDDL_Parser
from planning import search


class Planner:
    def __init__(self):
        pass

    # -----------------------------------------------
    # Solve
    # -----------------------------------------------

    def solve(self, domain_file, problem_file, heuristics, search_type):
        search_algo = search.ALGORITHMS[search_type]
        parser = self.parse(domain_file, problem_file)
        cost_estimate = None
        if search_algo != search.breadth_first_search:
            cost_estimate, _ = self.solve_relaxed_problem(heuristics, parser)
        return self.solve_informed_problem(cost_estimate, parser, search_algo)

    def parse(self, domain_file, problem_file):
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        return parser

    def solve_informed_problem(self, cost_estimate, parser, search_algo):
        problem = search.Problem(parser)
        # cost estimate for relaxed problem becomes guide for informed search
        problem.cost_estimate = cost_estimate
        return search_algo(problem)

    def solve_relaxed_problem(self, heuristics, parser):
        cost_estimate = -1
        problem = search.Problem(parser)
        # relax the original problem by altering the actions so that it's easier to solve.
        best_relaxed_problem = None
        for name in heuristics:
            heuristic_class = search.HEURISTIC_CLASS[name]
            heuristic = heuristic_class()
            for relaxed_problem in heuristic.configure(problem):
                relaxed_plan = search.breadth_first_search(relaxed_problem)
                if type(relaxed_plan) is list:
                    cost_estimate = max(cost_estimate, len(relaxed_plan))
                    best_relaxed_problem = relaxed_problem
        return cost_estimate, best_relaxed_problem


def parse_args(args):
    parser = argparse.ArgumentParser(description='Planning is discovering a sequence of actions that will achieve ' +
                                                 'a goal. This classical planner is compact, readable and designed ' +
                                                 'for educational purposes.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('domain_file', help='defines a problem domain via requirements, predicates, constants and '
                                            'actions using Planning Domain Definition Language (PDDL)')
    parser.add_argument('problem_file', help='defines problem by describing its domain, objects, initial state and '
                                             'goal state using Planning Domain Definition Language (PDDL)')
    parser.add_argument('-s', help='search algorithm used in the planner', dest='search_type',
                        choices=['bfs', 'astar'], default='bfs')
    # change to heuristics i.e., more than one
    parser.add_argument('-H', help="heuristics used in the search", dest='heuristics', action='append',
                        choices=['no_delete_effects', 'relaxed_preconds'])
    parser.add_argument('-v', '--verbose', help='gives verbose output for debugging purposes', action='store_true',
                        default=False)
    return parser.parse_args(args)


def run_planner():
    start_time = time.time()
    args = parse_args(sys.argv[1:])
    planner = Planner()
    plan = planner.solve(args.domain_file, args.problem_file, args.heuristics, args.search_type)
    print('Time: ' + str(time.time() - start_time) + 's')
    if type(plan) is list:
        print('plan:')
        for act in plan:
            print(act if args.verbose else act.name + ' ' + ' '.join(act.parameters))
    else:
        print('No plan was found')
        exit(1)


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    run_planner()
