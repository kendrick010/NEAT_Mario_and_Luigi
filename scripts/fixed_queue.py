class FixedQueue:

    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = []

    def push(self, item):
        if len(self.queue) == self.max_size:
            self.pop()

        self.queue.append(item)

    def pop(self):
        if len(self.queue):
            return self.queue.pop(0)
        
    def peek(self):
        if len(self.queue):
            return self.queue[0]
    
    def __repr__(self):
        # Return the list of items in the queue
        return f"{self.queue}"
    
    def __len__(self):
        return len(self.queue)