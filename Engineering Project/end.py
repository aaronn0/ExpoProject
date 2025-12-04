import pygame
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import database

pygame.init()
screen = pygame.display.set_mode((1200, 800))

font = pygame.font.Font("assets/font.ttf", 25)

testButton = database.Button(30, 30, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

button = database.Button(50, 650, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

click = pygame.mixer.Sound("assets/click.wav")

background = pygame.image.load("assets/happy.jpg")

background = pygame.transform.scale(background, screen.get_size())

text = [
    [
        font.render("Great job! You were able to save Grandpa!!", True, (0, 0, 0)),
        (600, 50),
        True
    ],
    [
        font.render("Thank you for playing!", True, (0, 0, 0)),
        (600, 120),
        True
    ],
    [
        font.render("Main Menu", True, (0, 200, 0)),
        (160, 690),
        False
    ]
]

def update():
    if button.click():
        click.play()
        return 0
    return 3

def draw():
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
    for i in text:
        database.blit_text(i, screen)

    screen.blit(button.display_image, button.rect)