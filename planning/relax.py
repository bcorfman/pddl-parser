import copy
from planning.util import frozenset_of_tuples, reduced_powerset


class RelaxPrecondition:
    def parameterize(self, problem):
        # create set of positive preconditions across all actions
        pos_set = set((act.positive_preconditions for act in problem.actions))

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
