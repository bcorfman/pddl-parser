from PDDL import PDDL_Parser

class Propositional_Planner:

    #-----------------------------------------------
    # Solve
    #-----------------------------------------------

    def solve(self, domain, problem):
        # Parser
        parser = PDDL_Parser()
        with open(domain,'r') as f:
            parser.parse_domain(f.read())
        with open(problem,'r') as f:
            parser.parse_problem(f.read())
        # Parsed data
        actions = parser.actions
        state = parser.state
        goal_pos = parser.positive_goals
        goal_not = parser.negative_goals
        # Do nothing
        if self.applicable(state, goal_pos, goal_not):
            return []
        # Search
        visited = [state]
        fringe = [state, None]
        while fringe:
            state = fringe.pop(0)
            plan = fringe.pop(0)
            for act in actions:
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                    new_state = self.apply(state, act)
                    if new_state not in visited:
                        if self.applicable(new_state, goal_pos, goal_not):
                            full_plan = [act]
                            while plan:
                                act, plan = plan
                                full_plan.insert(0, act)
                            return full_plan
                        visited.append(new_state)
                        fringe.append(new_state)
                        fringe.append((act, plan))
        return None

    #-----------------------------------------------
    # Applicable
    #-----------------------------------------------

    def applicable(self, state, positive, negative):
        for i in positive:
            if i not in state:
                return False
        for i in negative:
            if i in state:
                return False
        return True

    #-----------------------------------------------
    # Apply
    #-----------------------------------------------

    def apply(self, state, act):
        new_state = []
        for i in state:
            if i not in act.del_effects:
                new_state.append(i)
        for i in act.add_effects:
            if i not in new_state:
              new_state.append(i)
        return new_state

# ==========================================
# Main
# ==========================================
if __name__ == '__main__':
    import sys
    domain = sys.argv[1]
    problem = sys.argv[2]
    planner = Propositional_Planner()
    plan = planner.solve(domain, problem)
    print 'plan:'
    for act in plan:
        print act