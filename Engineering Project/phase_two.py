import pygame
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import database

pygame.init()
screen = pygame.display.set_mode((1200, 800))

font = pygame.font.SysFont("Arial", 40)

phase = 0

#INTRO
intro = [
    [
        font.render("Continue", True, (0, 200, 0)),
        (160, 670),
        False
    ]
]

background = [
    pygame.image.load("assets/heartpump.jpg")
]

#scale all backgrounds to size of screen
for i in range(len(background)):
    background[i] = pygame.transform.scale(background[i], screen.get_size())

cont = database.Button(50, 650, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

click = pygame.mixer.Sound("assets/click.wav")

def update():
    global phase
    if cont.click():
        phase += 1
        click.play()
    return 4

def draw():
    if phase == 0:
        screen.blit(background[0], screen.get_rect(topleft=(0, 0)))


    pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
    screen.blit(cont.display_image, cont.rect)
    database.blit_text(intro[0], screen)