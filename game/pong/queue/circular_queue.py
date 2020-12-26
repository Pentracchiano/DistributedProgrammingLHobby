import threading
from queue import Queue, Full


class CircularQueue:
    """
    Utility class for replacing old elements when the queue is full. Thread-safe.
    """
    def __init__(self, max_size: int):
        self.queue = Queue(max_size)
        self.lock = threading.Lock()

    def get(self):
        with self.lock:
            return self.queue.get()

    def put_nowait(self, item):
        with self.lock:
            try:
                self.queue.put_nowait(item)
            except Full:
                self.queue.get_nowait()
                self.queue.put_nowait(item)
