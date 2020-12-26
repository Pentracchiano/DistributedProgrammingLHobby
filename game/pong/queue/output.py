from game.pong.queue.circular_queue import CircularQueue


class QueueOutput:
    STATUS = 'status'
    INIT = 'init'
    END = 'end'

    def __init__(self, max_size: int):
        self.queue = CircularQueue(max_size)

    def __call__(self, game_status: dict):
        game_status_with_type = {'message_type': QueueOutput.STATUS}
        game_status_with_type.update(game_status)
        self.queue.put_nowait(game_status_with_type)

    def init(self, game_info: dict):
        game_info_with_type = {'message_type': QueueOutput.INIT}
        game_info_with_type.update(game_info)
        self.queue.put_nowait(game_info_with_type)

    def end_game(self, game_info: dict):
        game_info_with_type = {'message_type': QueueOutput.END}
        game_info_with_type.update(game_info)
        self.queue.put_nowait(game_info_with_type)
