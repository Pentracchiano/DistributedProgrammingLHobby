import pygame
import sys
from game.pong.paddle import PaddleCommand
import time
import websocket
import json
import threading
import queue

BALL_RADIUS = 0.02
PADDLE_HEIGHT = 0.13
PADDLE_WIDTH = 0.02
BLACK = 0, 0, 0
WHITE = 255, 255, 255

is_match_started = False
is_match_completed = False
is_socket_open = False
game_status_queue = queue.Queue()
output_queue = queue.Queue()

lock = threading.Condition()


def graphics_handler(ws):
    with lock:
        while not is_socket_open:
            lock.wait()

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

    while not is_match_completed:
        start = time.perf_counter()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if role != 'spectator':
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_LSHIFT]:
                if keys_pressed[pygame.K_w]:
                    output_queue.put(json.dumps({'command': 'fup'}))
                elif keys_pressed[pygame.K_s]:
                    output_queue.put(json.dumps({'command': 'fdown'}))
            elif keys_pressed[pygame.K_w]:
                output_queue.put(json.dumps({'command': 'up'}))
            elif keys_pressed[pygame.K_s]:
                output_queue.put(json.dumps({'command': 'down'}))

        try:
            message = game_status_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            screen = pygame.display.get_surface()
            screen.fill(BLACK)
            pygame.draw.circle(screen, WHITE, (message["ball_x"] * size[0],
                                               message["ball_y"] * size[1]), BALL_RADIUS * size[0])

            pygame.draw.rect(screen, WHITE,
                             pygame.rect.Rect(0, message["left_paddle_y"] * size[1] - PADDLE_HEIGHT / 2 * size[1],
                                              PADDLE_WIDTH * size[0], PADDLE_HEIGHT * size[1]))
            pygame.draw.rect(screen, WHITE,
                             pygame.rect.Rect(size[0] - PADDLE_WIDTH * size[0],
                                              message["right_paddle_y"] * size[1] - PADDLE_HEIGHT / 2 * size[1],
                                              PADDLE_WIDTH * size[0], PADDLE_HEIGHT * size[1]))
            pygame.display.flip()
        pygame.event.pump()
        end = time.perf_counter()
        elapsed = end - start
        remaining = 0.01 - elapsed
        time.sleep(remaining if remaining > 0 else 0)


def on_message(ws, message):
    global is_match_started, is_match_completed
    message = json.loads(message)
    if role in ['host', 'challenger'] and not is_match_started:
        print(message)
        with lock:
            is_match_started = message.get('message_type') == 'init'
            lock.notify()
    else:
        if message.get('message_type') == 'status':
            game_status_queue.put(message)
        elif message.get('message_type') == 'end':
            is_match_completed = True
            print(message)
            pygame.quit()
            sys.exit(0)


def on_error(ws, error):
    print(error.status_code)
    print(error.resp_headers)
    print(type(error))


def on_close(ws):
    print("closed")


def on_open(ws):
    global is_socket_open
    with lock:
        is_socket_open = True
        lock.notify()


def output_consumer(ws):
    while not is_match_completed:
        ws.send(output_queue.get())


if __name__ == '__main__':
    user = int(input("Select user: "))
    match_id = int(input("Insert match id: "))
    # width = int(input("Insert game window width: "))
    # height = int(input("Insert game window height: "))
    # role = input("Insert desired role: ")
    # token = input("Insert token: ")
    if user == 1:
        width = 1280
        height = 720
        role = 'challenger'
        token = '003d06d98879ee10bf1c45040003c90fc5b53c47'
    elif user == 2:
        width = 800
        height = 600
        role = 'host'
        token = 'da76aaf23ab38f59aaa6337cdb82ed3b25f0bbb4'
    else:
        width = 640
        height = 320
        role = 'spectator'
        token = '06c033109641ce67f16a422661323d93c8f858cd'

    size = width, height
    socket = websocket.WebSocketApp(f'ws://localhost:8000/ws/game/{match_id}/?role={role}',
                                    on_message=on_message, on_error=on_error, on_close=on_close,
                                    header={"Authorization": f"Token {token}"},
                                    on_open=on_open)

    pygame.init()
    pygame.display.set_mode(size)
    threading.Thread(target=socket.run_forever).start()
    if role != 'spectator':
        threading.Thread(target=output_consumer, args=(socket, )).start()
    graphics_handler(socket)
