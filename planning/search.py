import copy
import time
from planning.util import Queue, PriorityQueue, frozenset_of_tuples
from planning import relax
from planning import heuristic


class Node:
    def __init__(self, state, cost=None, actions=None):
        self.state = frozenset_of_tuples(state)
        self._cost = cost
        self.actions = tuple(actions) if actions is not None else tuple()

    def __copy__(self, other):
        return Node(other.state, other.cost, other.actions)

    @property
    def cost(self):
        return self._cost or len(self.actions)


class Problem:
    def __init__(self, parser=None, heuristic_class=None):
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

        self.cost_estimate = None

        if parser and heuristic_class:
            self.relaxed = heuristic_class(parser)
        else:
            self.relaxed = self

    def __copy__(self):
        other = Problem()
        other.name = self.name
        other.state = self.state.copy()
        other.positive_goals = self.positive_goals.copy()
        other.negative_goals = self.negative_goals.copy()
        other.cost = self.heuristic(other.state)
        other.requirements = self.requirements[:]
        other.types = self.types.copy()
        other.objects = self.objects.copy()
        other.predicates = self.predicates.copy()
        other.relaxed = copy.copy(self.relaxed) if self.relaxed is not self else self
        other.actions = [copy.copy(act) for act in self.actions]
        other.ground_actions = []
        other.cost_estimate = self.cost_estimate
        return other

    def groundify_actions(self):
        # Grounding process
        self.ground_actions = []
        for action in self.actions:
            for act in action.groundify(self.objects, self.types):
                self.ground_actions.append(act)

    def applicable(self, node, positive, negative):
        return positive.issubset(node.state) and negative.isdisjoint(node.state)

    def apply(self, node, action):
        new_state = node.state.difference(action.del_effects).union(action.add_effects)
        new_cost = node.cost + action.cost + self.relaxed.heuristic(new_state)
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

    def heuristic(self, state):
        """
        A heuristic function estimates the cost from the current state to the nearest
        goal in the provided search problem.
        """
        if self.cost_estimate is not None:
            return (self.cost_estimate - len(self.positive_goals.intersection(state)) +
                    len(self.negative_goals.difference(state)))
        else:
            return len(self.positive_goals.difference(state)) + len(self.negative_goals.intersection(state))


def graph_search(frontier, problem, max_time):
    visited = set()
    initial_state = problem.state
    initial_cost = problem.relaxed.heuristic(initial_state)
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
        if node.state not in visited:
            visited.add(node.state)
            for new_node in problem.generate_successors(node):
                if new_node.state not in visited:
                    frontier.push(new_node)


def breadth_first_search(problem, max_time):
    """Search the shallowest nodes in the search tree first."""
    frontier = Queue()
    return graph_search(frontier, problem, max_time)


def astar_search(problem, max_time):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = PriorityQueue()
    return graph_search(frontier, problem, max_time)


ALGORITHMS = {'bfs': breadth_first_search,
              'astar': astar_search}

RELAXING_TRANSFORMATIONS = {'preconds': relax.RelaxPrecondition,
                            'no_delete_effects': relax.RelaxDeleteEffects}

HEURISTIC_CLASS = {'max': heuristic.h_max,
                   'add': heuristic.h_add}
