import random

import pygame
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import phase_one
import phase_two
import menu
import end

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 800))

pygame.display.set_caption("ENGINEERING PROJECT")


running = True

font = pygame.font.SysFont("Arial", 60)

clock = pygame.time.Clock()

num_states = 0

while running:
    dt = clock.tick(60)/1000
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # RENDER YOUR GAME HERE
    if num_states == 0:
        num_states = menu.update()
        menu.draw()
    elif num_states == 1:
        num_states = phase_one.update()
        phase_one.draw()
    elif num_states == 3:
        num_states = end.update()
        end.draw()
    elif num_states == 4:
        num_states = phase_two.update(dt)
        phase_two.draw()
    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()

