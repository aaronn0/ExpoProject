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

button = database.Button(100, 360, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

text = [
    [
        font.render("Great Diagnosis! Continue to the Pico Portion", True, (255, 255, 255)),
        (600, 50),
        True
    ],
    [
        font.render("to Save Grandpa!", True, (255, 255, 255)),
        (600, 120),
        True
    ],
    [
        font.render("Main Menu", True, (255, 255, 255)),
        (200, 355),
        False
    ]
]

def update():
    if button.click():
        return 0
    return 3

def draw():
    screen.fill("black")
    for i in text:
        database.blit_text(i, screen)

    screen.blit(button.display_image, button.rect)