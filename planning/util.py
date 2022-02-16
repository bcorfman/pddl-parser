from collections import deque
from itertools import combinations, repeat, starmap
import operator


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    def is_empty(self):
        return len(self._data) == 0


class Queue:
    def __init__(self):
        self._data = deque()

    def push(self, item):
        self._data.appendleft(item)

    def pop(self):
        return self._data.pop()

    def is_empty(self):
        return len(self._data) == 0


class PriorityQueue:
    def __init__(self):
        self._data = []
        self._count = 0

    def push(self, item, priority):
        entry = (priority, self._count, item)
        heapq.heappush(self._data, entry)
        self._count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self._data)
        return item

    def is_empty(self):
        return len(self._data) == 0

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


def smaller_subslices(seq):
    """ Return all contiguous non-empty subslices of a sequence, except the longest.
    Used for generating sequences of relaxed preconditions."""
    # smaller_subslices('ABCD') --> A AB ABC B BC BCD C CD D
    items = list(seq)
    length = len(seq)
    slices = starmap(slice, ((x, y) for x, y in combinations(range(length + 1), 2) if y - x < length))
    return map(operator.getitem, repeat(items), slices)
