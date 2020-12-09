from game.pong.game_rules import Position
import enum


class PaddleCommand(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    FAST_UP = enum.auto()
    FAST_DOWN = enum.auto()
    NO_INPUT = enum.auto()


class Paddle:

    def __init__(self, position: Position, speed: float, width: float, height: float,
                 acceleration: float, acceleration_factor: float, braking_factor: float):
        self.position = position
        self.speed = speed
        self.height = height
        self.width = width
        self.acceleration = acceleration
        self.acceleration_factor = acceleration_factor
        self.braking_factor = braking_factor

    def move(self, delta_t: float, command: PaddleCommand):
        if command == PaddleCommand.UP:
            self.speed += self.acceleration
        elif command == PaddleCommand.FAST_UP:
            self.speed += self.acceleration * self.acceleration_factor
        elif command == PaddleCommand.DOWN:
            self.speed -= self.acceleration
        elif command == PaddleCommand.FAST_DOWN:
            self.speed -= self.acceleration * self.acceleration_factor
        elif command == PaddleCommand.NO_INPUT:
            self.speed /= self.braking_factor

        self.position.y += self.speed * delta_t

        margin_reached = self.field_margin_reached()
        if margin_reached:
            self.position.y = 1 - self.height/2 if margin_reached > 0 else self.height/2
            self.speed = 0

        return margin_reached

    def field_margin_reached(self):
        if self.position.y + self.height / 2 >= 1:
            return 1
        elif self.position.y - self.height / 2 <= 0:
            return -1
        else:
            return 0
