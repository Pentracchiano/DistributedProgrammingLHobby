from game.pong.ball import Ball
from game.pong.game_rules import *
from game.pong.paddle import Paddle
import threading
import time


class Controller:
    def __init__(self, input, output):
        self.input = input
        self.output = output

        self.paddle_left = Paddle(
            position=Position2D(0+PADDLE_WIDTH/2, 0.5),
            speed=0,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            acceleration=0.1,
            acceleration_fast_factor=3,
            braking_factor=1.5
        )
        self.paddle_right = Paddle(
            position=Position2D(1-PADDLE_WIDTH/2, 0.5),
            speed=0,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            acceleration=0.1,
            acceleration_fast_factor=3,
            braking_factor=1.5
        )
        self.ball = self.create_ball(going_right=True)

        self.sudden_death = False

        self.left_score = 0
        self.right_score = 0

        self.game_tick_time = 0.01

        self.match_time = 0
        self.MAX_MATCH_TIME = 5 * 60

        self.output.init({
            "ball_radius": BALL_RADIUS,
            "paddle_height": PADDLE_HEIGHT,
            "paddle_width": PADDLE_WIDTH
        })

        self.stop = False
        self.game_thread = threading.Thread(target=self.run_game)
        self.game_thread.start()

    def run_game(self):
        while not self.stop:
            current_time = time.perf_counter()

            self.update_game()
            if self.left_score >= 5 or self.right_score >= 5:
                self.send_results()
                return
            if self.match_time > self.MAX_MATCH_TIME:
                if self.left_score != self.right_score:
                    self.send_results()
                    return
                else:
                    self.sudden_death = True

            end_time = time.perf_counter()
            elapsed = end_time - current_time
            remaining = self.game_tick_time - elapsed
            if remaining > 0:
                self.match_time += self.game_tick_time
                time.sleep(remaining)
            else:
                self.match_time += elapsed

    def update_game(self):
        left_paddle_input = self.input.left_paddle_input
        right_paddle_input = self.input.right_paddle_input

        left_paddle_margin_reached = self.paddle_left.move(self.game_tick_time, left_paddle_input)
        right_paddle_margin_reached = self.paddle_right.move(self.game_tick_time, right_paddle_input)

        has_bounced = self.ball.move(self.game_tick_time)

        if self.ball.position.x < 0:
            self.right_score += 1
            self.ball = self.create_ball(going_right=False)
        elif self.ball.position.x > 1:
            self.left_score += 1
            self.ball = self.create_ball(going_right=True)

        self.output({
            "has_bounced": has_bounced,
            "left_paddle_margin_reached": left_paddle_margin_reached,
            "right_paddle_margin_reached": right_paddle_margin_reached,
            "left_score": self.left_score,
            "right_score": self.right_score,
            "left_paddle_y": self.paddle_left.position.y,
            "right_paddle_y": self.paddle_right.position.y,
            "ball_x": self.ball.position.x,
            "ball_y": self.ball.position.y,
            "match_time": int(self.match_time),
            "sudden_death": self.sudden_death
        })

    def send_results(self):
        self.output.end_game({
            "left_score": self.left_score,
            "right_score": self.right_score,
            "match_time": self.match_time
        })

    def stop_game(self):
        self.stop = True
        self.game_thread.join()

    def create_ball(self, going_right: bool):
        return Ball(
            position=Position2D(INITIAL_POSITION_X, INITIAL_POSITION_Y),
            speed=Speed2D(INITIAL_SPEED_X, INITIAL_SPEED_Y) if going_right else Speed2D(-INITIAL_SPEED_X, INITIAL_SPEED_Y),
            radius=BALL_RADIUS,
            paddle_left=self.paddle_left,
            paddle_right=self.paddle_right
        )



