import pygame
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import database

pygame.init()
screen = pygame.display.set_mode((1200, 800))

testButton = database.Button(30, 30, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

font = pygame.font.Font("assets/font.ttf", 25)

click = pygame.mixer.Sound("assets/click.wav")

button = database.Button(100, 200, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

text = [
    [
        font.render("EXPO PROJECT", True, (255, 255, 255)),
        (600, 50),
        True
    ],
    [
        font.render("Play Game", True, (255, 255, 255)),
        (200, 225),
        False
    ]
]

def update():
    if button.click():
        click.play()
        return 1
    return 0

def draw():
    screen.fill("black")
    for i in text:
        database.blit_text(i, screen)
    screen.blit(button.display_image, button.rect)
