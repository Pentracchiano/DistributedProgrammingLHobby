from game.pong.game_rules import Position2D, Speed2D
from game.pong.paddle import Paddle


class Ball:

    def __init__(self, position: Position2D, speed: Speed2D, radius: float,
                 paddle_left: Paddle, paddle_right: Paddle):
        self.position = position
        self.speed = speed
        self.radius = radius
        self.paddle_left = paddle_left
        self.paddle_right = paddle_right

    def move(self, delta_t: float) -> bool:
        self.position.x += self.speed.x * delta_t
        self.position.y += self.speed.y * delta_t

        if self.speed.x > 0:
            paddle = self.paddle_right
        else:
            paddle = self.paddle_left

        has_bounced = False
        if self.check_paddle_collision(paddle):
            self.speed.x *= -1
            self.speed.y = self.position.y - paddle.position.y + paddle.speed
            has_bounced = True
        elif self.position.y - self.radius <= 0 or self.position.y + self.radius >= 1:
            self.speed.y *= -1
            has_bounced = True

        return has_bounced

    def check_paddle_collision(self, paddle: Paddle) -> bool:
        return ((self.position.y <= paddle.position.y + self.radius + paddle.height / 2
                 or self.position.y >= paddle.position.y - self.radius - paddle.height / 2)
                and (
                        self.position.x <= paddle.position.x + paddle.width + self.radius
                        or self.position.x <= paddle.position.x - paddle.width - self.radius
                ))
