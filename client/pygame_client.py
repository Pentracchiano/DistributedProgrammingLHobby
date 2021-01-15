import pygame
import sys
from game.pong.paddle import PaddleCommand
import time
import websocket
import json
import threading

BALL_RADIUS = 0.02
PADDLE_HEIGHT = 0.13
PADDLE_WIDTH = 0.02
BLACK = 0, 0, 0
WHITE = 255, 255, 255

is_match_started = False
is_match_completed = False
lock = threading.Condition()


def input_handler(ws):
    if role == 'host':
        with lock:
            while not is_match_started:
                input("Press ENTER to start the match")
                ws.send(json.dumps({'command': 'start_match'}))
                lock.wait()

    elif role == 'challenger':
        with lock:
            if not is_match_started:
                input("Ready to play? Press ENTER")
                ws.send(json.dumps({'command': 'ready'}))
                lock.wait()
    else:
        return

    while not is_match_completed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LSHIFT]:
            if keys_pressed[pygame.K_w]:
                ws.send(json.dumps({'command': 'fup'}))
            elif keys_pressed[pygame.K_s]:
                ws.send(json.dumps({'command': 'fdown'}))
        elif keys_pressed[pygame.K_w]:
            ws.send(json.dumps({'command': 'up'}))
        elif keys_pressed[pygame.K_s]:
            ws.send(json.dumps({'command': 'down'}))

        time.sleep(0.01)
        pygame.event.pump()


def on_message(ws, message):
    global is_match_started
    message = json.loads(message)
    if role in ['host', 'challenger'] and not is_match_started:
        print(message)
        with lock:
            is_match_started = message.get('message_type') == 'init'
            lock.notify()
    else:
        if message.get('message_type') == 'status':
            screen.fill(BLACK)
            pygame.draw.circle(screen, WHITE, (message["ball_x"] * size[0],
                                                    message["ball_y"] * size[1]), BALL_RADIUS)

            pygame.draw.rect(screen, WHITE,
                             pygame.rect.Rect(0, message["left_paddle_y"] * size[1] - PADDLE_HEIGHT / 2,
                                              PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.rect(screen, WHITE,
                             pygame.rect.Rect(size[0] - PADDLE_WIDTH,
                                              message["right_paddle_y"] * size[1] - PADDLE_HEIGHT / 2,
                                              PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.display.flip()
        elif message.get('message_type') == 'end':
            print(message)
            sys.exit(0)


def on_error(ws, error):
    print(error.status_code)
    print(error.resp_headers)
    print(type(error))


def on_close(ws):
    print("closed")


def on_open(ws):
    global screen
    screen = pygame.display.set_mode(size)


if __name__ == '__main__':

    match_id = int(input("Insert match id: "))
    width = int(input("Insert game window width: "))
    height = int(input("Insert game window height: "))
    role = input("Insert desired role: ")
    token = input("Insert token: ")

    size = width, height

    socket = websocket.WebSocketApp(f'ws://localhost:8000/ws/game/{match_id}/?role={role}',
                                    on_message=on_message, on_error=on_error, on_close=on_close,
                                    header={"Authorization": f"Token {token}"},
                                    on_open=on_open)

    socket.run_forever()
