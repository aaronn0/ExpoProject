import pygame
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import database

pygame.init()
screen = pygame.display.set_mode((1200, 800))

font = pygame.font.Font("assets/font.ttf", 25)

phase = 0

failed = 0

health = 0

#INTRO
intro = [
    [
        font.render("Continue", True, (0, 200, 0)),
        (160, 690),
        False
    ],
    [
        [
            font.render("It looks like Grandpa's heart pump is", True, (0, 0, 0)),
            (500, 100),
            False
        ],
        [
            font.render("malfunctioning...", True,
                        (0, 0, 0)),
            (500, 160),
            False
        ]
    ],
    [
        [
            font.render("A heart pump is used to pump blood in", True, (0, 0, 0)),
            (500, 100),
            False
        ],
        [
            font.render("someone's body when their heart is too weak", True,(0, 0, 0)),
            (500, 160),
            False
        ],
        [
            font.render("However, they can malfunction if they", True,(0, 0, 0)),
            (640, 300),
            False
        ],
        [
            font.render("are improperly designed.", True,(0, 0, 0)),
            (640, 360),
            False
        ]
    ],
    [
        [
            font.render("For now, let's try to keep Grandpa stable by performing CPR on him.", True, (0, 0, 0)),
            (50, 50),
            False
        ],
        [
            font.render("Use the physical button on the heart below to perform compressions.", True, (0, 0, 0)),
            (50, 110),
            False
        ],
        [
            font.render("Time your button presses when the                are in the", True, (0, 0, 0)),
            (50, 170),
            False
        ],
        [
            font.render("red bars", True, (255, 0, 0)),
            (573, 170),
            False
        ],
        [
            font.render("blue bar!", True, (0, 130, 255)),
            (860, 170),
            False
        ]

    ],
    [
        [
            font.render(f"{failed}/7 failed compressions.", True, (255, 0, 0)),
            (50, 50),
            False
        ],
        [
            font.render(f"{health}/30 successful compressions.", True, (0, 200, 100)),
            (50, 110),
            False
        ],
        [
            font.render("(Failing 7 compressions makes you lose!)", True, (0, 0, 0)),
            (50, 170),
            False
        ]
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

heart = []

for i in range(6):
    heart.append(pygame.image.load(f"assets/heart{i + 1}.png"))

barend = pygame.image.load("assets/barend.png")
barmid = pygame.image.load("assets/barmid.png")

barmid = pygame.transform.scale(barmid, (900, 64))

timing = pygame.image.load("assets/timing.png")

selection = pygame.surface.Surface((60, 400), pygame.SRCALPHA)
selection.fill((0, 100, 100, 100))
container = pygame.image.load("assets/selectcontainer.png")

timings = []
wait = 0

def update(delta):
    global phase, wait, timings
    if phase < 3:
        if cont.click():
            phase += 1
            click.play()
            if phase == 2:
                cont.rect = cont.rect.move((0, -340))
                intro[0][1] = (160, 350)
                intro[0][0] = font.render("Start", True, (0, 200, 0))
    elif phase == 3:
        wait += delta
        with open("data.txt", "r") as f:
            temp = f.readlines()
            lines = []
            for i in temp:
                lines.append(i.strip())

            pressed = lines[0] == "1"

        if wait >= 0.6:
            wait = 0
            timings.append(database.Timing(delta))


    return 4

def draw():
    global phase
    if phase < 2:
        screen.blit(background[0], screen.get_rect(topleft=(0, 0)))
        for t in intro[phase + 1]:
            database.blit_text(t, screen)
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
        screen.blit(cont.display_image, cont.rect)
        database.blit_text(intro[0], screen)
    elif phase == 2 or phase == 3:
        screen.fill((255, 255, 255))
        for t in intro[phase + 1]:
            database.blit_text(t, screen)
        screen.blit(barmid, barmid.get_rect(topleft = (0, 500)))
        screen.blit(barend, barend.get_rect(topleft = (900, 500)))
        screen.blit(selection, selection.get_rect(center = (800, 532)))
        screen.blit(container, container.get_rect(center = (800, 532)))

        screen.blit(heart[health//6], heart[health//6].get_rect(center = (1070, 532)))

        if phase == 2:
            pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 300, 320, 110))
            screen.blit(cont.display_image, cont.rect)
            database.blit_text(intro[0], screen)