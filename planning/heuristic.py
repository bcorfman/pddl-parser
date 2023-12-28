# TODO: Question: 1) eval relaxed preconditions as well, 2) hash problem, then return to this h if PDDL
#  hasn't changed?
# TODO: Need h init function to set up any metadata, plus an update function for metadata to be updated
# TODO: when a node is expanded
from collections import Counter


def h_null(_predicates):
    return 0


def h_max(predicates):
    counter = Counter(predicates)
    return max(counter.values())


def h_add(predicates):
    counter = Counter(predicates)
    return sum(counter.values())


TYPES = {'max': h_max,
         'add': h_add}
