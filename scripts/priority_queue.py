import heapq

class FixedLengthPriorityQueue:

    def __init__(self, max_length):
        self.max_length = max_length
        self.heap = []

    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))

        if len(self.heap) > self.max_length: heapq.heappop(self.heap)

    def pop(self):
        _, item = heapq.heappop(self.heap)
        return item
    
    def __repr__(self):
        return f"{self.heap}"