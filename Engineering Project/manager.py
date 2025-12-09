"""
Modified: 8 December 2025
By Aaron Noh

Purpose: Switch between different gamestates and update the pygame display to match.
"""
import pygame
import os

#sets current working directory to current file folder, allows this file to be run even if moving from computer to computer
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#imports all the other game phases
import phase_one
import phase_two
import menu
import end

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("ENGINEERING PROJECT")
running = True

#set up clock
clock = pygame.time.Clock()

#saves current state of game in variable
num_states = 0

while running:
    #saves current delta time in dt variable
    dt = clock.tick(60)/1000

    #quits pygame properly if the X button on the top right of window is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #switches between gamestates depending on num_states
    if num_states == 0:
        #.update() returns a number that corresponds with their num_states
        #if game wants to switch between states, .update() returns a different number

        #updates current gamestate according to menu
        num_states = menu.update()
        #draws the corresponding gamestate
        menu.draw()
    elif num_states == 1:
        #updates current gamestate according to phase 1
        num_states = phase_one.update()
        phase_one.draw()
        #draws the corresponding gamestate
    elif num_states == 2:
        #updates current gamestate according to phase 2
        num_states = phase_two.update(dt)
        #draws the corresponding gamestate
        phase_two.draw()
    elif num_states == 3:
        #updates current gamestate according to end
        num_states = end.update()
        #draws the corresponding gamestate
        end.draw()
    # flip() the display to put work on screen
    pygame.display.flip()

#quits pygame when game stops running
pygame.quit()

