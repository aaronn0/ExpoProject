import pygame
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import game
import learn
import menu
import end

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 800))

pygame.display.set_caption("ENGINEERING PROJECT")

running = True

font = pygame.font.SysFont("Arial", 60)

num_states = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE
    if num_states == 0:
        num_states = menu.update()
        menu.draw()
    if num_states == 1:
        num_states = game.update()
        game.draw()
    if num_states == 2:
        num_states = learn.update()
        learn.draw()
    if num_states == 3:
        num_states = end.update()
        end.draw()
    # flip() the display to put your work on screen
    pygame.display.flip()

      # limits FPS to 60

pygame.quit()

