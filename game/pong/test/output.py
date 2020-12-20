import pygame
import sys

BLACK = 0, 0, 0
WHITE = 255, 255, 255


class PygameOutput:
    def __init__(self, width: int, height: int):
        self.size = width, height
        self.screen = pygame.display.set_mode(self.size)
        self.ball_radius = None
        self.paddle_height = None
        self.paddle_width = None

    def __call__(self, game_status: dict):
        print(game_status)
        self.screen.fill(BLACK)
        pygame.draw.circle(self.screen, WHITE, (game_status["ball_x"] * self.size[0],
                                                game_status["ball_y"] * self.size[1]), self.ball_radius)

        pygame.draw.rect(self.screen, WHITE,
                         pygame.rect.Rect(0, game_status["left_paddle_y"] * self.size[1] - self.paddle_height / 2,
                                          self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.screen, WHITE,
                         pygame.rect.Rect(self.size[0]-self.paddle_width, game_status["right_paddle_y"] * self.size[1] - self.paddle_height / 2,
                                          self.paddle_width, self.paddle_height))

        pygame.display.flip()

    def init(self, game_info: dict):
        self.ball_radius = int(game_info["ball_radius"] * self.size[1])
        self.paddle_height = int(game_info["paddle_height"] * self.size[1])
        self.paddle_width = int(game_info["paddle_width"] * self.size[0])

    def end_game(self, game_info: dict):
        print(game_info)
        sys.exit(0)
