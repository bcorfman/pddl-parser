import copy
import math
import time
from .util import Queue, PriorityQueue, frozenset_of_tuples
from .heuristic import h_null


class Node:
    def __init__(self, state, cost=None, actions=None):
        self.state = frozenset_of_tuples(state)
        self.cost = cost
        self.actions = tuple(actions) if actions is not None else tuple()

    def __copy__(self, other):
        return Node(other.state, other.cost, other.actions)

    def __lt__(self, other):
        return self.cost < other.cost


class Problem:
    def __init__(self, parser=None, heuristic=h_null):
        if parser:
            self.name = parser.problem_name
            self.state = parser.state.copy()
            self.positive_goals = parser.positive_goals.copy()
            self.negative_goals = parser.negative_goals.copy()
            self.requirements = parser.requirements[:]
            self.types = parser.types.copy()
            self.objects = parser.objects.copy()
            self.predicates = parser.predicates.copy()
            self.actions = parser.actions
            self.groundify_actions()
        else:
            self.name = ""
            self.state = frozenset()
            self.positive_goals = frozenset()
            self.negative_goals = frozenset()
            self.requirements = []
            self.types = frozenset()
            self.objects = frozenset()
            self.predicates = frozenset()
            self.actions = []
            self.ground_actions = []

        self.heuristic = heuristic
        self.solution = []

    def __copy__(self):
        other = Problem()
        other.name = self.name
        other.state = self.state.copy()
        other.positive_goals = self.positive_goals.copy()
        other.negative_goals = self.negative_goals.copy()
        other.requirements = self.requirements[:]
        other.types = self.types.copy()
        other.objects = self.objects.copy()
        other.predicates = self.predicates.copy()
        other.actions = [copy.copy(act) for act in self.actions]
        other.ground_actions = []
        other.heuristic = self.heuristic
        other.solution = self.solution[:]
        return other

    def __str__(self):
        return 'Problem: ' + self.name + \
               '\n  positive_goals: ' + str([list(i) for i in self.positive_goals]) + \
               '\n  negative_goals: ' + str([list(i) for i in self.negative_goals]) + \
               '\n  actions: ' + str([list(i) for i in self.actions])

    def groundify_actions(self):
        """ Turns all actions into ground actions.
        Returns :: None. """
        self.ground_actions = []
        for action in self.actions:
            for act in action.groundify(self.objects, self.types):
                self.ground_actions.append(act)

    def applicable(self, node, positive, negative):
        return positive.issubset(node.state) and negative.isdisjoint(node.state)

    def apply(self, node, action):
        new_state = node.state.difference(action.del_effects).union(action.add_effects)
        new_cost = node.cost + self.heuristic(new_state)
        return Node(new_state, new_cost, list(node.actions) + [action])

    def at_goal(self, node):
        return self.positive_goals.issubset(node.state) and self.negative_goals.isdisjoint(node.state)

    def generate_successors(self, node):
        new_nodes = []
        for action in self.ground_actions:
            if self.applicable(node, action.positive_preconditions, action.negative_preconditions):
                new_node = self.apply(node, action)
                new_nodes.append(new_node)
        return new_nodes


def graph_search(frontier, problem, max_time):
    visited = set()
    initial_state = problem.state
    initial_cost = problem.heuristic(initial_state)
    frontier.push(Node(initial_state, initial_cost))
    expanded = 0
    start_time = time.time()
    while not frontier.is_empty() and (time.time() - start_time) < max_time:
        node = frontier.pop()
        expanded += 1
        if problem.at_goal(node):
            print(f"expanded nodes: {expanded}")
            print(f"unexpanded nodes: {frontier.count}")
            return list(node.actions)
        visited.add(node.state)
        for new_node in problem.generate_successors(node):
            if new_node.state not in visited and new_node not in frontier:
                frontier.push(new_node)
            elif new_node in frontier:
                del frontier[new_node]
                frontier.push(new_node)


def breadth_first_search(problem, max_time=60):
    """Search the shallowest nodes in the search tree first."""
    frontier = Queue()
    return graph_search(frontier, problem, max_time)


def astar_search(problem, max_time=60):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = PriorityQueue()
    return graph_search(frontier, problem, max_time)


INFORMED_SEARCHES = {'astar': astar_search}
UNINFORMED_SEARCHES = {'bfs': breadth_first_search}
ALGORITHMS = INFORMED_SEARCHES | UNINFORMED_SEARCHES
