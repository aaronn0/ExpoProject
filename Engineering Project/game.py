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

#create backgrounds
background = [
    pygame.image.load("assets/oldguynormal.jpg"),
    pygame.image.load("assets/heartattack.jpg"),
    pygame.image.load("assets/ground.jpg"),
    pygame.image.load("assets/paper.png")
]

#scale all backgrounds to size of screen
for i in range(len(background)):
    background[i] = pygame.transform.scale(background[i], screen.get_size())

#create a transparent layer
trans_back = pygame.surface.Surface(screen.get_size(), pygame.SRCALPHA)
trans_back.fill((0, 0, 0, 125))

#create intro text that will show up
intro = [
    [
        font.render("This is Grandpa.", True, (0, 0, 0)),
        (80, 80),
        False
    ],
    [
        font.render("Oh No! Grandpa's Collapsed!", True, (0, 0, 0)),
        (80, 80),
        False
    ]
]

paper_text = [
    [
        font.render("Normal Vitals", True, (0, 0, 0)),
        (560, 260),
        True
    ],
    [
        font.render("Grandpa's Vitals", True, (0, 0, 0)),
        (840, 260),
        True
    ],
    [
        font.render("Core Temp", True, (0, 0, 0)),
        (325, 360),
        True
    ],
    [
        font.render("Heart Rate", True, (0, 0, 0)),
        (325, 460),
        True
    ],
    [
        font.render("Breaths/Min", True, (0, 0, 0)),
        (325, 560),
        True
    ],
    [
        font.render("Blood Oxygen", True, (0, 0, 0)),
        (325, 660),
        True
    ],
    [
        font.render("Bld Pressure", True, (0, 0, 0)),
        (325, 760),
        True
    ]
]

table = [
    pygame.rect.Rect(690, 220, 5, 570),
    pygame.rect.Rect(430, 220, 5, 570),
    pygame.rect.Rect(240, 290, 730, 5),
    pygame.rect.Rect(240, 410, 730, 5),
    pygame.rect.Rect(240, 510, 730, 5),
    pygame.rect.Rect(240, 610, 730, 5),
    pygame.rect.Rect(240, 700, 730, 5),
]

#create buttons
button = [
    database.Button(130, 320, pygame.image.load("assets/select1.png"), pygame.image.load("assets/select1.png")),
    database.Button(130, 430, pygame.image.load("assets/select2.png"), pygame.image.load("assets/select2.png")),
    database.Button(130, 520, pygame.image.load("assets/select1.png"), pygame.image.load("assets/select1.png")),
    database.Button(130, 625, pygame.image.load("assets/select3.png"), pygame.image.load("assets/select3.png")),
    database.Button(130, 720, pygame.image.load("assets/select2.png"), pygame.image.load("assets/select2.png"))
]
cont = database.Button(50, 650, pygame.image.load("assets/continue1.png"), pygame.image.load("assets/continue2.png"))

selected = [
    False,
    False,
    False,
    False,
    False
]

confirm = pygame.image.load("assets/confirm.png")

def update():
    global phase
    if phase < 3:
        if cont.click():
            phase += 1

    if phase == 3:
        for i in range(len(selected)):
            if button[i].click():
                selected[i] = not selected[i]

    return 1

def draw():
    global phase
    if phase < 3:
        screen.blit(background[phase], screen.get_rect(topleft = (0, 0)))
        screen.blit(cont.display_image, cont.rect)
    elif phase == 3:
        screen.blit(background[2], screen.get_rect(topleft = (0, 0)))
        screen.blit(trans_back, screen.get_rect(topleft = (0, 0)))
        screen.blit(background[phase], screen.get_rect(topleft = (0, 0)))

    if phase == 0:
        database.blit_text(intro[0], screen)
    elif phase == 2:
        pygame.draw.rect(screen, (255, 255, 255), intro[1][0].get_rect(topleft=intro[1][1]))
        database.blit_text(intro[1], screen)
    elif phase == 3:
        for i in paper_text:
            database.blit_text(i, screen)
        for i in button:
            screen.blit(i.display_image, i.rect)
        for i in table:
            pygame.draw.rect(screen, (0, 0, 0), i)
        for i in range(len(selected)):
            if selected[i]:
                screen.blit(confirm, button[i].rect)