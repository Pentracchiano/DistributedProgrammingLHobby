from game.pong.test.output import PygameOutput
from game.pong.test.input import Input
from game.pong.controller import Controller
import pygame
import sys
from game.pong.paddle import PaddleCommand
import time

if __name__ == '__main__':
    #todo crearne uno simile ma con websocket
    input = Input()
    output = PygameOutput(1280, 720)
    controller = Controller(input, output)
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
