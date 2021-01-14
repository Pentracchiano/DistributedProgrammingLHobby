try:
    import thread
except ImportError:
    import _thread as thread

import pygame
import sys
from game.pong.paddle import PaddleCommand
import time
import websocket
import json


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error.status_code)
    print(error.resp_headers)
    print(type(error))


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send(json.dumps({'command': 'ready'}))
    ws.send(json.dumps({'command': 'start_match'}))


if __name__ == '__main__':

    match_id = int(input("Insert match id: "))
    role = input("Insert desired role: ")
    token = input("Insert token: ")

    socket = websocket.WebSocketApp(f'ws://localhost:8000/ws/game/{match_id}/?role={role}',
                                    on_message=on_message, on_error=on_error, on_close=on_close,
                                    header={"Authorization": f"Token {token}"},
                                    on_open=on_open)

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
