import heapq
import operator
from collections import deque
from itertools import combinations


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
                self.data.append((priority, c, item))
                heapq.heapify(self.data)
                break
        else:
            self.push(item, priority)


def frozenset_of_tuples(data):
    return frozenset([tuple(item) for item in data])


def subslices(seq):
    """ Return all contiguous non-empty subslices of a sequence """
    # subslices('ABCD') --> A AB ABC ABCD B BC BCD C CD D
    slices = starmap(slice, combinations(range(len(seq) + 1), 2))
    return map(operator.getitem, repeat(seq), slices)
