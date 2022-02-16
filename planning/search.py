
import copy
from itertools import product
from planning.util import Queue, PriorityQueue, frozenset_of_tuples, smaller_subslices


class Node:
    def __init__(self, state, cost, actions=None):
        self.state = frozenset_of_tuples(state)
        self.cost = cost
        self.actions = tuple(actions) if actions is not None else tuple()

    def __copy__(self, other):
        return Node(other.state, other.cost, other.actions)


class Problem:
    def __init__(self, parser):
        self.name = parser.problem_name
        self.state = parser.state.copy()
        self.positive_goals = parser.positive_goals.copy()
        self.negative_goals = parser.negative_goals.copy()
        self.cost = self.heuristic(self.state)
        self.requirements = parser.requirements.copy()
        self.types = parser.types.copy()
        self.objects = parser.objects.copy()
        self.predicates = parser.predicates.copy()
        self.ground_actions = self._groundify_actions(parser.actions)

    def _groundify_actions(self, actions):
        # Grounding process
        ground_actions = []
        for action in actions:
            for act in action.groundify(self.objects, self.types):
                ground_actions.append(act)
        return ground_actions

    def applicable(self, node, positive, negative):
        return positive.issubset(node.state) and negative.isdisjoint(node.state)

    def apply(self, node, action):
        new_state = node.state.difference(action.del_effects).union(action.add_effects)
        return Node(new_state, node.cost + action.cost, list(node.actions) + [action])

    def at_goal(self, node):
        return self.positive_goals.issubset(node.state) and self.negative_goals.isdisjoint(node.state)

    def generate_relaxed_actions_with_fewer_preconditions(self, act):
        for pos, neg in product(smaller_subslices(act.positive_preconditions),
                                smaller_subslices(act.negative_preconditions)):
            action = copy.copy(act)
            action.positive_preconditions = pos
            action.negative_preconditions = neg
            yield action

    def generate_relaxed_action_without_delete_effects(self, act):
        action = copy.copy(act)
        action.del_effects = []
        return action

    def generate_successors(self, node):
        new_nodes = []
        for action in self.ground_actions:
            if self.applicable(node, action.positive_preconditions, action.negative_preconditions):
                new_node = self.apply(node, action)
                new_nodes.append(new_node)
        return new_nodes

    def heuristic(self, _state):
        """
        A heuristic function estimates the cost from the current state to the nearest
        goal in the provided search problem.  This heuristic is trivial.
        """
        return 0  # null heuristic by default


def graph_search(frontier, problem):
    visited = set()
    initial_state = problem.state
    initial_cost = problem.heuristic(initial_state)
    frontier.push(Node(initial_state, initial_cost))

    while not frontier.is_empty():
        node = frontier.pop()
        if problem.at_goal(node):
            return list(node.actions)
        if node.state not in visited:
            visited.add(node.state)
            for new_node in problem.generate_successors(node):
                if new_node.state not in visited:
                    frontier.push(new_node)


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = Queue()
    return graph_search(frontier, problem)


def astar_search(problem):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = PriorityQueue()
    return graph_search(frontier, problem)
