BALL_RADIUS = 0.02
INITIAL_SPEED_X = 0.5
INITIAL_SPEED_Y = 0.288
INITIAL_POSITION_X = 0.5
INITIAL_POSITION_Y = 0.5
PADDLE_HEIGHT = 0.13
PADDLE_WIDTH = 0.02
RIGHT_PADDLE_X = 1 - PADDLE_WIDTH/2
LEFT_PADDLE_X = 0 + PADDLE_WIDTH/2


class Position2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Speed2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
