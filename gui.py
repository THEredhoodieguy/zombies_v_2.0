#written for python 3.0+
#Matthew Pletcher 2017

import pygame
from agents import *

#colors used from PICO-8 default pallette
BLACK      = (  0,   0,   0)
DARKBLUE   = ( 29,  43,  83)
DARKPURPLE = (126,  37,  83)
DARKGREEN  = (  0, 135,  81)
BROWN      = (171,  82,  54)
DARKGRAY   = ( 95,  87,  79)
LIGHTGRAY  = (194, 195, 199)
WHITE      = (255, 241, 232)
RED        = (255,   0,  77)
ORANGE     = (255, 163,   0)
YELLOW     = (255, 236,  39)
GREEN      = (  0, 228,  54)
BLUE       = ( 41, 173, 255)
INDIGO     = (131, 118, 156)
PINK       = (255, 119, 168)
PEACH      = (255, 204, 170)

class Game(object):

    def __init__(self, xbound, ybound, num_blocks, num_humans, num_zombies):

        pygame.init()

        sim = Simulator(num_humans, num_zombies, xbound, ybound, num_blocks)
        sim.start_processes()

        width = xbound * 10
        height = ybound * 10

        WINDOW_SIZE = [width, height]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        myfont = pygame.font.Font(None, 30)

        clock = pygame.time.Clock()

        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill(WHITE)

            humans = sim.get_humans()
            zombies = sim.get_zombies()

            for i in zombies:
                pygame.draw.rect(screen,
                    RED,
                    [math.floor(i.x * 10),
                    math.floor(i.y * 10), 
                    10, 10
                    ])

            for i in humans:
                pygame.draw.rect(screen,
                    BLUE,
                    [math.floor(i.x * 10),
                    math.floor(i.y * 10), 
                    10, 10
                    ])

            clock.tick(30)

            sim.update()

            pygame.display.update()

        sim.end_processes()
        pygame.quit()


if __name__ == "__main__":
    game = Game(100, 100, 4, 500, 30)