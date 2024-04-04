import time

class FixedQueue:

    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = []
        self.timestamps = []

    def push(self, item):
        if len(self.queue) == self.max_size:
            self.pop()

        self.timestamps.append(time.time())
        self.queue.append(item)

    def pop(self):
        if self.queue:
            self.timestamps.pop(0)
            return self.queue.pop(0)
        
    def peek(self):
        if self.queue:
            return self.queue[0], self.timestamps[0]
    
    def __repr__(self):
        # Return the list of items in the queue
        return f"{self.queue}"