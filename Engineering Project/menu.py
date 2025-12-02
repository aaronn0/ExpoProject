import pygame
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import database

pygame.init()
screen = pygame.display.set_mode((1200, 800))

font = pygame.font.SysFont("Arial", 60)

testButton = database.Button(30, 30, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

font = pygame.font.SysFont("Arial", 40)

buttons = [
    database.Button(100, 200, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png")),
    database.Button(100, 500, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png")),
]

text = [
    [
        font.render("Group 8 Milestone 3", True, (255, 255, 255)),
        (600, 50),
        True
    ],
    [
        font.render("Play Game", True, (255, 255, 255)),
        (200, 195),
        False
    ],
    [
        font.render("Learn More About Heart Pumps", True, (255, 255, 255)),
        (200, 505),
        False
    ]
]

def update():
    if buttons[0].click():
        return 1
    if buttons[1].click():
        return 2
    return 0

def draw():
    screen.fill("black")
    for i in text:
        database.blit_text(i, screen)
    for i in buttons:
        screen.blit(i.display_image, i.rect)
