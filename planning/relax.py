import copy
from collections import Counter, defaultdict
from planning.search import Problem, Node
from planning.util import frozenset_of_tuples, reduced_powerset


class RelaxedProblem(Problem):
    def __init__(self, heuristic):
        super().__init__()
        self.linked_facts, self.precond_count = self._link_facts()
        self.subtraction = Counter()
        self.estimated_num_actions = heuristic()

    def _link_facts(self):
        precond_count = Counter(dict((act, len(act.positive_preconditions)) for act in self.ground_actions))
        facts = defaultdict(list)
        for act in self.ground_actions:
            assert not act.negative_preconditions
            for p in act.positive_preconditions | act.add_effects:
                facts[p].append(act)
        return facts, precond_count

    def applicable(self, node, positive, negative):
        assert not negative
        self.subtraction = Counter(dict((self.linked_facts[item], -1) for item in node.state))
        self.precond_count += self.subtraction
        return any((self.precond_count[k] <= 0 for k in self.subtraction.keys()))

    def apply(self, node, action):
        new_state = node.state.union(action.add_effects)
        new_cost = node.cost + self.h(new_state)
        return Node(new_state, new_cost, list(node.actions) + [action])

    def generate_successors(self, node):
        new_nodes = []
        for action in self.ground_actions:
            if self.applicable(node, action.positive_preconditions, action.negative_preconditions):
                new_node = self.apply(node, action)
                new_nodes.append(new_node)
        return new_nodes

    def h(self, state):
        return self.estimated_num_actions - len(state)


class RelaxPrecondition:
    def parameterize(self, problem):
        # create set of positive preconditions across all actions
        pos_set = frozenset_of_tuples((act.positive_preconditions for act in problem.actions))

        # create combinations of a reduced set of positive preconditions,
        # and for each of these combos, create a new problem to evaluate.
        for predicates in reduced_powerset(pos_set):
            yield self.apply(problem, predicates)  # TODO: write test for this

    def apply(self, problem, predicates):
        if not predicates:
            raise ValueError("cannot relax action preconditions with an empty predicate.")
        pred_set = frozenset_of_tuples(predicates)
        new_problem = copy.copy(problem)
        for act in new_problem.actions:
            if act.negative_preconditions:
                raise ValueError("predicate cannot be applied to actions with negative preconditions.")
            act.positive_preconditions = act.positive_preconditions - pred_set
            act.add_effects = act.add_effects - pred_set
            act.del_effects = act.del_effects - pred_set
        new_problem.positive_goals = new_problem.positive_goals - pred_set
        return new_problem


class RelaxDeleteEffects:
    def apply(self, problem, _predicates=None):
        new_problem = copy.copy(problem)
        for action in new_problem.actions:
            action.del_effects = []
        return new_problem


TRANSFORMATIONS = {'preconds': RelaxPrecondition,
                   'no_delete_effects': RelaxDeleteEffects}
