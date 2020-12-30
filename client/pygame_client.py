try:
    import thread
except ImportError:
    import _thread as thread

import pygame
import sys
from game.pong.paddle import PaddleCommand
import time
import websocket


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


if __name__ == '__main__':

    match_id = int(input("Insert match id: "))
    role = input("Insert desired role: ")

    socket = websocket.WebSocketApp(f'ws://localhost:8000/ws/game/{match_id}/?role={role}',
                                    on_message=on_message, on_error=on_error, on_close=on_close)

    socket.run_forever()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LSHIFT]:
            if keys_pressed[pygame.K_w]:
                input.left_paddle_input = PaddleCommand.FAST_UP
            elif keys_pressed[pygame.K_s]:
                input.left_paddle_input = PaddleCommand.FAST_DOWN
        elif keys_pressed[pygame.K_w]:
            input.left_paddle_input = PaddleCommand.UP
        elif keys_pressed[pygame.K_s]:
            input.left_paddle_input = PaddleCommand.DOWN

        if keys_pressed[pygame.K_RSHIFT]:
            if keys_pressed[pygame.K_UP]:
                input.right_paddle_input = PaddleCommand.FAST_UP
            elif keys_pressed[pygame.K_DOWN]:
                input.right_paddle_input = PaddleCommand.FAST_DOWN
        elif keys_pressed[pygame.K_UP]:
            input.right_paddle_input = PaddleCommand.UP
        elif keys_pressed[pygame.K_DOWN]:
            input.right_paddle_input = PaddleCommand.DOWN

        time.sleep(0.01)
        pygame.event.pump()
