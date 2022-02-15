from collections import deque


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
