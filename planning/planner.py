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

    def solve(self, domain_file, problem_file, problem_class, search_algo):
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        problem = problem_class(parser)
        return search_algo(problem)


def parse_args(args):
    parser = argparse.ArgumentParser(description='Planning is discovering a sequence of actions that will achieve ' +
                                                 'a goal. This classical planner is compact, readable and designed ' +
                                                 'for educational purposes.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('domain_file', help='defines a problem domain via requirements, predicates, constants and '
                                            'actions using Planning Domain Definition Language (PDDL)')
    parser.add_argument('problem_file', help='defines problem by describing its domain, objects, initial state and '
                                             'goal state using Planning Domain Definition Language (PDDL)')
    parser.add_argument('-a', help='search algorithm used in the planner', dest='search_algo',
                        default=search.breadth_first_search)
    parser.add_argument('-p', help="problem class used in the search", dest='problem_class', default=search.Problem)
    parser.add_argument('-v', '--verbose', help='gives verbose output for debugging purposes', action='store_true',
                        default=False)
    return parser.parse_args(args)


def run_planner():
    start_time = time.time()
    args = parse_args(sys.argv[1:])
    planner = Planner()
    plan = planner.solve(args.domain_file, args.problem_file, args.problem_class, args.search_algo)
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
