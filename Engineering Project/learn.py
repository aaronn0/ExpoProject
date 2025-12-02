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

text = [
    [
        font.render("ABOUT HEART PUMPS", True, (255, 255, 255)),
        (600, 50),
        True
    ],
    [
        font.render("="*50, True, (255, 255, 255)),
        (600, 120),
        True
    ],
    [
        font.render("A mechanical heart pump (also called a ventricular assist device) helps pump", True, (255, 255, 255)),
        (600, 190),
        True
    ],
    [
        font.render("blood when someone's heart is weak.", True, (255, 255, 255)),
        (600, 260),
        True
    ],
    [
        font.render("- Too SLOW: Not enough blood reaches the body", True, (255, 255, 255)),
        (600, 330),
        True
    ],
    [
        font.render("- Too FAST: Can damage blood cells and organs", True, (255, 255, 255)),
        (600, 400),
        True
    ],
    [
        font.render("That's why engineers test their designs many times!", True, (255, 255, 255)),
        (600, 470),
        True
    ],
    [
        font.render("="*50, True, (255, 255, 255)),
        (600, 540),
        True
    ]
]
#background = pygame.image.load("assets/background.png")

items = [testButton]

def update():
    if testButton.click():
        return 0
    return 2

def draw():
    screen.fill("black")
    for i in items:
        screen.blit(i.display_image, i.rect)

    for i in text:
        database.blit_text(i, screen)