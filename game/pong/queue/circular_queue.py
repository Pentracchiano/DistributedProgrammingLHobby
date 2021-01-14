import threading
from collections import deque


class CircularQueue:
    """
    Utility class for replacing old elements when the queue is full. Thread-safe.
    """
    def __init__(self, max_size: int):
        self.queue = deque(maxlen=max_size)
        self.lock = threading.Condition()

    def get(self):
        with self.lock:
            while len(self.queue) < 1:
                self.lock.wait()
            return self.queue.popleft()

    def put_nowait(self, item):
        with self.lock:
            self.queue.append(item)
            self.lock.notify()
