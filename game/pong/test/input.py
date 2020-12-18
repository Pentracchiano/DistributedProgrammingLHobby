from game.pong.paddle import PaddleCommand
import threading


class Input:
    def __init__(self):
        self._left_paddle_input = PaddleCommand.NO_INPUT
        self._right_paddle_input = PaddleCommand.NO_INPUT
        self.left_lock = threading.Lock()
        self.right_lock = threading.Lock()

    @property
    def left_paddle_input(self):
        with self.left_lock:
            ret = self._left_paddle_input
            self._left_paddle_input = PaddleCommand.NO_INPUT

        return ret

    @property
    def right_paddle_input(self):
        with self.right_lock:
            ret = self._right_paddle_input
            self._right_paddle_input = PaddleCommand.NO_INPUT

        return ret

    @left_paddle_input.setter
    def left_paddle_input(self, value):
        with self.left_lock:
            self._left_paddle_input = value

    @right_paddle_input.setter
    def right_paddle_input(self, value):
        with self.right_lock:
            self._right_paddle_input = value
