from planning.util import Queue, PriorityQueue, frozenset_of_tuples


class Node:
    def __init__(self, state, cost, actions=None):
        self.state = frozenset_of_tuples(state)
        self.cost = cost
        self.actions = tuple(actions) if actions is not None else tuple()

    def __copy__(self, other):
        return Node(other.state, other.cost, other.actions)


class Domain:
    def __init__(self, parser):
        self.name = parser.domain_name
        self.requirements = parser.requirements
        self.types = parser.types
        self.objects = parser.objects
        self.actions = parser.actions
        self.predicates = parser.predicates
        self.ground_actions = self._groundify_actions()

    def _groundify_actions(self):
        # Grounding process
        ground_actions = []
        for action in self.actions:
            for act in action.groundify(self.objects, self.types):
                ground_actions.append(act)
        return ground_actions


class Problem:
    def __init__(self, parser):
        self.name = parser.problem_name
        self.state = parser.state.copy()
        self.positive_goals = parser.positive_goals.copy()
        self.negative_goals = parser.negative_goals.copy()
        self.cost = self.heuristic(self.state)

    def applicable(self, node, positive, negative):
        return positive.issubset(node.state) and negative.isdisjoint(node.state)

    def apply(self, node, action):
        new_state = node.state.difference(action.del_effects).union(action.add_effects)
        return Node(new_state, node.cost + action.cost, list(node.actions) + [action])

    def at_goal(self, node):
        return self.positive_goals.issubset(node.state) and self.negative_goals.isdisjoint(node.state)

    def heuristic(self, _state):
        """
        A heuristic function estimates the cost from the current state to the nearest
        goal in the provided search problem.  This heuristic is trivial.
        """
        return 0  # null heuristic by default


def successors(node, domain, problem):
    new_nodes = []
    for action in domain.ground_actions:
        if problem.applicable(node, action.positive_preconditions, action.negative_preconditions):
            new_node = problem.apply(node, action)
            new_nodes.append(new_node)
    return new_nodes


def graph_search(frontier, domain, problem):
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
            for new_node in successors(node, domain, problem):
                if new_node.state not in visited:
                    frontier.push(new_node)


def breadth_first_search(domain, problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = Queue()
    return graph_search(frontier, domain, problem)


def astar_search(domain, problem):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = PriorityQueue()
    return graph_search(frontier, domain, problem)


