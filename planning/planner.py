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
import copy
import math
import sys
import time
from planning import search
from planning.PDDL import PDDL_Parser
from planning.util import partition
from planning import relax, heuristic


class Planner:
    def __init__(self, max_time=60):
        self.max_time = max_time
        self.search_algo = None
        self.transforms = []
        self.best_relaxed_problem = None
        self.best_plan = None
        self.best_time = math.inf

    # -----------------------------------------------
    # Solve
    # -----------------------------------------------

    def solve(self, domain_file, problem_file, transformations, heuristic_type, search_type, max_time):
        self.max_time = max_time
        search_algo = search.ALGORITHMS[search_type]
        transforms = [relax.TRANSFORMATIONS[name] for name in transformations]
        parser = self.parse(domain_file, problem_file)
        if heuristic_type and search_type in search.INFORMED_SEARCHES:
            h = heuristic.TYPES[heuristic_type]
            problem = relax.RelaxedProblem(h)
            plan = self.solve_informed(problem, transforms, search_algo)
        else:
            problem = search.Problem(parser)
            plan = search_algo(problem, self.max_time)
        return plan

    def parse(self, domain_file, problem_file):
        parser = PDDL_Parser()
        parser.parse_domain(domain_file)
        parser.parse_problem(problem_file)
        return parser

    def solve_informed(self, problem, transforms, search_algo):
        relaxed_problem = self.relax_problem(problem, transforms)
        relaxed_plan = search_algo(relaxed_problem, self.max_time)
        return relaxed_plan

    def relax_problem(self, problem, transforms):
        # relax the original problem by altering the actions so that it's easier to solve.
        updated_problem = copy.copy(problem)
        apply_transforms, parameterize_transforms = partition(lambda obj: hasattr(obj, 'parameterize'), transforms)
        while apply_transforms:
            transform_class = apply_transforms.pop()
            updated_problem = self.apply_relaxation(updated_problem, transform_class)
        while parameterize_transforms:
            transform_class = parameterize_transforms.pop()
            updated_problem = self.evaluate_relaxation(updated_problem, transform_class)
        updated_problem.groundify_actions()
        return updated_problem

    def apply_relaxation(self, relaxed_problem, transform_class):
        transform = transform_class()
        return transform.apply(relaxed_problem)

    def reset_eval(self):
        self.best_relaxed_problem = None
        self.best_plan = None
        self.best_time = math.inf

    def evaluate_relaxation(self, problem, transform_class):
        self.reset_eval()
        transform = transform_class()
        for trial_problem in transform.parameterize(problem):
            trial_problem.groundify_actions()
            self.eval_search(trial_problem)
        else:
            if self.best_plan is None:
                raise Exception("Could not find a best relaxed solution.")
        print(self.best_relaxed_problem)
        return self.best_relaxed_problem

    def eval_search(self, trial_problem):
        start_time = time.time()
        trial_plan = self.search_algo(trial_problem, self.max_time)
        trial_time = time.time() - start_time
        if trial_plan and trial_time < self.best_time:
            self.best_relaxed_problem = trial_problem
            self.best_plan = trial_plan
            self.best_relaxed_problem.solution = self.best_plan
            self.best_time = trial_time


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
                        choices=search.ALGORITHMS.keys(), default=list(search.ALGORITHMS.keys()).pop())
    parser.add_argument('-R', help='transformations to relax the problem for heuristic search', dest='transformations',
                        choices=relax.TRANSFORMATIONS.keys(), action='append')
    parser.add_argument('-H', help="heuristic used in the search", dest='heuristic_type',
                        choices=heuristic.TYPES.keys())
    parser.add_argument('-t', help="maximum time used for search (in seconds)", dest="max_time", type=int, default=60)
    parser.add_argument('-v', '--verbose', help='gives verbose output for debugging purposes', action='store_true',
                        default=False)
    return parser.parse_args(args)


def run_planner():
    start_time = time.time()
    args = parse_args(sys.argv[1:])
    planner = Planner()
    plan = planner.solve(args.domain_file, args.problem_file, args.transformations, args.heuristic_type,
                         args.search_type, args.max_time)
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
