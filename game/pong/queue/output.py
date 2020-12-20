from collections import deque


class QueueOutput:
    def __init__(self, max_size: int):
        self.queue = deque(maxlen=max_size)
        self.init_game_info = None
        self.end_game_info = None

    def __call__(self, game_status: dict):
        self.queue.append(game_status)

    def init(self, game_info: dict):
        self.init_game_info = game_info

    def end_game(self, game_info: dict):
        self.end_game_info = game_info
