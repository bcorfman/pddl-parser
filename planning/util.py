import heapq
from collections import deque
from itertools import chain, combinations, tee, filterfalse


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item, _priority=None):
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    def is_empty(self):
        return self.count == 0

    def count(self):
        return len(self._data)


class Queue:
    def __init__(self):
        self._data = deque()

    def push(self, item, _priority=None):
        self._data.appendleft(item)

    def pop(self):
        return self._data.pop()

    def is_empty(self):
        return self.count == 0

    @property
    def count(self):
        return len(self._data)


class PriorityQueue:
    def __init__(self):
        self._data = []
        self._count = 0

    def push(self, item, priority=None):
        if priority is None:
            priority = item.cost
        entry = (priority, self._count, item)
        heapq.heappush(self._data, entry)
        self._count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self._data)
        return item

    def is_empty(self):
        return self.count == 0

    @property
    def count(self):
        return len(self._data)

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self._data):
            if i == item:
                if p <= priority:
                    break
                del self._data[index]
                self._data.append((priority, c, item))
                heapq.heapify(self._data)
                break
        else:
            self.push(item, priority)


def frozenset_of_tuples(data):
    return frozenset([tuple(item) for item in data])


def powerset(iterable):
    """ powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3) """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def reduced_powerset(seq):
    if type(seq) != set:
        seq = frozenset(seq)
    return frozenset_of_tuples((seq - frozenset(x) for x in powerset(seq) if 0 < len(x) < len(seq)))


def partition(pred, iterable):
    """Use a predicate to partition entries into false entries and true entries"""
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return list(filterfalse(pred, t1)), list(filter(pred, t2))
