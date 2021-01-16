import pygame
import sys
import time
import websocket
import json
import threading
import queue
import requests
import PyInquirer
from enum import IntEnum


class Questions(IntEnum):
    LOGIN = 0
    USERNAME = 1
    PASSWORD = 2
    CREATE_USERNAME = 3
    CREATE_PASSWORD = 4
    ROLE = 5
    WIDTH = 6
    HEIGHT = 7


def validate_integer(value):
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


questions = [
    {
        'type': 'list',
        'name': Questions.LOGIN.name,
        'message': 'Do you want to sign-in or sign-up?',
        'choices': ['Sign in', 'Sign up'],
    },
    {
        'type': 'input',
        'name': Questions.USERNAME.name,
        'message': 'Enter your username:',
    },
    {
        'type': 'password',
        'name': Questions.PASSWORD.name,
        'message': 'Enter your password:',
    },
    {
        'type': 'input',
        'name': Questions.CREATE_USERNAME.name,
        'message': 'Create an username:',
    },
    {
        'type': 'password',
        'name': Questions.CREATE_PASSWORD.name,
        'message': 'Create your password:',
    },
    {
        'type': 'list',
        'name': Questions.ROLE.name,
        'message': 'What do you want to be? Choose your role:',
        'choices': ['host', 'challenger', 'spectator'],
    },
    {
        'type': 'input',
        'name': Questions.WIDTH.name,
        'message': 'Choose screen width:',
        'validate': validate_integer,
        'filter': int
    },
    {
        'type': 'input',
        'name': Questions.HEIGHT.name,
        'message': 'Choose screen height:',
        'validate': validate_integer,
        'filter': int
    },
]


BALL_RADIUS = 0.02
PADDLE_HEIGHT = 0.13
PADDLE_WIDTH = 0.02
BLACK = 0, 0, 0
WHITE = 255, 255, 255

API_ENDPOINT = 'http://127.0.0.1:8000/api/'

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


def login():
    answers = PyInquirer.prompt(questions[Questions.LOGIN])

    if answers[Questions.LOGIN.name] == 'Sign in':
        q_user = Questions.USERNAME
        q_pw = Questions.PASSWORD
        url = API_ENDPOINT + 'token/'

    else:
        q_user = Questions.CREATE_USERNAME
        q_pw = Questions.CREATE_PASSWORD
        url = API_ENDPOINT + 'users/sign_up/'

    answers.update(PyInquirer.prompt([questions[q_user], questions[q_pw]]))
    data = {
        'username': answers[q_user.name],
        'password': answers[q_pw.name]
    }
    res = requests.post(url=url, data=data)
    res_dict = res.json()
    if res.status_code != requests.codes.ok and res.status_code != requests.codes.created:
        for key in res_dict.keys():
            for value in res_dict[key]:
                print('Error: ' + value)
        sys.exit(0)

    try:
        return res_dict["token"]
    except KeyError:
        url = API_ENDPOINT + 'token/'
        res = requests.post(url=url, data=data)
        res_dict = res.json()
        return res_dict["token"]


def choose_role():
    answer = PyInquirer.prompt(questions[Questions.ROLE])
    return answer[Questions.ROLE.name]


def get_match_id(user_session, user_role):
    url = API_ENDPOINT + 'ongoing_matches/'
    if user_role == 'host':
        res = user_session.post(url=url)
        if res.status_code != requests.codes.created:
            print(res.text)
            sys.exit(0)
        else:
            return res.json()['id']

    else:
        if user_role == 'challenger':
            params = {'is_full': False}
            message = 'Choose a match. Only matches waiting for challengers are displayed:'
        else:
            params = None
            message = 'Choose a match to spectate:'
        q_name = 'ongoing_match'
        res = user_session.get(url=url, params=params)
        matches = res.json()
        choices = []

        for match in matches:
            challenger = match['challenger']
            if challenger:
                challenger_string = f"Challenger {match['challenger']['username']} ({match['challenger']['elo']})"
            else:
                challenger_string = "Waiting for challenger"
            choices.append({
                'name': f"Host: {match['host']['username']} ({match['host']['elo']}) - "
                        f"{challenger_string} - "
                        f"Number of spectators: {len(match['spectators'])} - "
                        f"{'Started' if match['is_started'] else 'Not started'}",
                'value': match['id']
            })

        if len(choices) == 0:
            print("No matches available at this moment, maybe you can try to host a match.")
            sys.exit(0)

        question = {
            'type': 'list',
            'name': q_name,
            'message': message,
            'choices': choices,
            'pageSize': 10
        }

        answer = PyInquirer.prompt(question)

    return answer[q_name]


if __name__ == '__main__':
    token = login()
    session = requests.Session()
    session.headers.update({"Authorization": f"Token {token}"})

    role = choose_role()
    match_id = get_match_id(session, role)

    answers = PyInquirer.prompt([questions[Questions.WIDTH], questions[Questions.HEIGHT]])

    size = answers[Questions.WIDTH.name], answers[Questions.HEIGHT.name]

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
