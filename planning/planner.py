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
from planning import search
from planning.PDDL import PDDL_Parser
from planning.util import partition


class Planner:
    def __init__(self):
        self.max_time = 60

    # -----------------------------------------------
    # Solve
    # -----------------------------------------------

    def solve(self, domain_file, problem_file, transformations, heuristic_type, search_type, max_time):
        self.max_time = max_time
        search_algo = search.ALGORITHMS[search_type]
        parser = self.parse(domain_file, problem_file)
        cost_estimate = None
        if heuristic_type and search_algo != search.breadth_first_search:
            cost_estimate, _ = self.solve_relaxed_problem(parser, search_algo, transformations, heuristic_type)
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
        return search_algo(problem, self.max_time)

    def solve_relaxed_problem(self, parser, search_algo, transformations, heuristic_type):
        cost_estimate = -1
        problem = search.Problem(parser)
        relaxed_problem = self.relax_problem(parser, search_algo, transformations, heuristic_type)
        heuristic_class = search.HEURISTIC_CLASS[heuristic_type]
        heuristic = heuristic_class(problem.state)
        relaxed_plan = search_algo(relaxed_problem, self.max_time)
        if type(relaxed_plan) is list:
            cost_estimate = max(cost_estimate, len(relaxed_plan))
            best_relaxed_problem = relaxed_problem
        return cost_estimate, relaxed_problem

    def relax_problem(self, parser, search_algo, transformations, heuristic_type):
        # relax the original problem by altering the actions so that it's easier to solve.
        updated_problem = search.Problem(parser)
        transforms = [search.RELAXING_TRANSFORMATIONS[name] for name in transformations]
        apply_transforms, parameterize_transforms = partition(lambda obj: hasattr(obj, 'parameterize'), transforms)
        while apply_transforms:
            transform_class = apply_transforms.pop()
            updated_problem = self.apply_relaxation(transform_class, updated_problem)
        while parameterize_transforms:
            transform_gen = parameterize_transforms.pop()
            updated_problem = self.evaluate_relaxation(updated_problem, transform_gen, search_algo)
        return updated_problem

    def apply_relaxation(self, transform_class, relaxed_problem):
        transform = transform_class()
        return transform.apply(relaxed_problem)

    def evaluate_relaxation(self, problem, transform_gen, search_algo):
        best_relaxed_problem = None
        best_time = math.inf
        start_time = 0
        for transform_class in transform_gen:
            transform = transform_class()
            for trial_problem in transform.parameterize(problem):
                trial_problem.groundify_actions()
                start_time = time.time()
                trial_plan = search_algo(trial_problem, self.max_time)
                trial_time = time.time() - start_time
                if trial_plan and trial_time < best_time:
                    best_relaxed_problem = trial_problem
                    best_time = trial_time
        else:
            if best_relaxed_problem is None and start_time == 0:
                raise Exception("Could not find any relaxed solution.")
        return best_relaxed_problem


def parse_args(args):
    parser = argparse.ArgumentParser(description='Planning is discovering a sequence of actions that will achieve ' +
                                                 'a goal. This classical planner is compact, readable and designed ' +
                                                 'for educational purposes.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('domain_file', help='defines a problem domain via requirements, predicates, constants and '
                                            'actions using Planning Domain Definition Language (PDDL)')
    parser.add_argument('problem_file', help='defines problem by describing its domain, objects, initial state and '
                                             'goal state using Planning Domain Definition Language (PDDL)')
    parser.add_argument('-S', help='search algorithm used in the planner', dest='search_type',
                        choices=['bfs', 'astar'], default='bfs')
    parser.add_argument('-R', help='transformations to relax the problem for heuristic search', dest='transformations',
                        choices=search.RELAXING_TRANSFORMATIONS.keys(), action='append')
    parser.add_argument('-H', help="heuristic used in the search", dest='heuristic_type', choices=['max', 'sum'])
    parser.add_argument('-t', help="maximum time used for search (in seconds)", dest="max_time", type=int, default=60)
    parser.add_argument('-v', '--verbose', help='gives verbose output for debugging purposes', action='store_true',
                        default=False)
    return parser.parse_args(args)


def run_planner():
    start_time = time.time()
    args = parse_args(sys.argv[1:])
    planner = Planner()
    plan = planner.solve(args.domain_file, args.problem_file, args.transformations, args.heuristic_type, args.search_type,
                         args.max_time)
    print('Time: ' + str(time.time() - start_time) + 's')
    if type(plan) is list:
        print(f'plan length: {len(plan)}')
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
