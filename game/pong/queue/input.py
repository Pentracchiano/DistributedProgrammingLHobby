from game.pong.paddle import PaddleCommand
from collections import deque


class QueueInput:
    def __init__(self, max_size: int):
        self.left_queue = deque(maxlen=max_size)
        self.right_queue = deque(maxlen=max_size)

    @property
    def left_paddle_input(self):
        return QueueInput._consume_input(self.left_queue)

    @property
    def right_paddle_input(self):
        return QueueInput._consume_input(self.right_queue)

    @left_paddle_input.setter
    def left_paddle_input(self, value):
        self.left_queue.append(value)

    @right_paddle_input.setter
    def right_paddle_input(self, value):
        self.right_queue.append(value)

    @staticmethod
    def _consume_input(queue: deque):
        try:
            return queue.popleft()
        except IndexError:
            return PaddleCommand.NO_INPUT
