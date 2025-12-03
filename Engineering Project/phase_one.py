import pygame
import random
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

#INTRO
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
    ],
    [
        font.render("Continue", True, (0, 200, 0)),
        (160, 670),
        False
    ]

]

cont = database.Button(50, 650, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

#PAPER DIAGNOSIS
paper_text = [
    [
        font.render("Normal Vitals", True, (0, 0, 0)),
        (560, 260),
        True
    ],
    [
        font.render("98.6F", True, (0, 0, 0)),
        (560, 360),
        True
    ],
    [
        font.render("60-100 bpm", True, (0, 0, 0)),
        (560, 460),
        True
    ],
    [
        font.render("12-8", True, (0, 0, 0)),
        (560, 560),
        True
    ],
    [
        font.render("95-100%", True, (0, 0, 0)),
        (560, 660),
        True
    ],
    [
        font.render("120/80 mmHg", True, (0, 0, 0)),
        (560, 760),
        True
    ],
    [
        font.render("Grandpa's Vitals", True, (0, 0, 0)),
        (840, 260),
        True
    ],
    [
        font.render("98.6F", True, (0, 0, 0)),
        (840, 360),
        True
    ],
    [
        font.render("40 bpm", True, (0, 0, 0)),
        (840, 460),
        True
    ],
    [
        font.render("0", True, (0, 0, 0)),
        (840, 560),
        True
    ],
    [
        font.render("80%", True, (0, 0, 0)),
        (840, 660),
        True
    ],
    [
        font.render("80/50 mmHg", True, (0, 0, 0)),
        (840, 760),
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
        font.render("Blood Pressure", True, (0, 0, 0)),
        (325, 760),
        True
    ]
]

top_text = [
    font.render("Let's see what's wrong with Grandpa.", True, (0, 0, 0)),
    (50, 50),
    False
]
bot_text = [
    font.render("Compare each set of vitals and mark down if they are different.", True, (0, 0, 0)),
    (50, 120),
    False
]
sub_text = [
        font.render("Submit", True, (0, 200, 0)),
        (800, 45),
        False
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

p1_button = [
    database.Button(130, 320, pygame.image.load("assets/select1.png"), pygame.image.load("assets/select1.png")),
    database.Button(130, 430, pygame.image.load("assets/select2.png"), pygame.image.load("assets/select2.png")),
    database.Button(130, 520, pygame.image.load("assets/select1.png"), pygame.image.load("assets/select1.png")),
    database.Button(130, 625, pygame.image.load("assets/select3.png"), pygame.image.load("assets/select3.png")),
    database.Button(130, 720, pygame.image.load("assets/select2.png"), pygame.image.load("assets/select2.png")),
    database.Button(930, 25, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))
]

p2_button = [
    database.Button(60, 105, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png")),
    database.Button(310, 105, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png")),
    database.Button(560, 105, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))
]

p2_text = [
    [
        font.render("Heart", True, (0, 200, 0)),
        (180, 125),
        False
    ],
    [
        font.render("Legs", True, (20, 80, 230)),
        (440, 125),
        False
    ],
    [
        font.render("Head", True, (200, 0, 0)),
        (680, 125),
        False
    ]
]

selected = [False, False, False, False, True]
correct = [False, True, True, True, True]

confirm = pygame.image.load("assets/confirm.png")
mark = pygame.image.load("assets/mark.png")

hints = [
    "Maybe look at his heartrate?",
    "That wouldn't explain his lack of breathing.",
    "His heartrate seems strangely low..."
]

wrong = pygame.mixer.Sound("assets/wrong.wav")
write = pygame.mixer.Sound("assets/write.wav")
right = pygame.mixer.Sound("assets/right.wav")
click = pygame.mixer.Sound("assets/click.wav")

def update():
    global phase, selected
    if phase < 3:
        if cont.click():
            click.play()
            phase += 1
    elif phase == 3:
        for i in range(len(selected)):
            if p1_button[i].click():
                write.play()
                selected[i] = not selected[i]
        if p1_button[5].click():
            if selected == correct:
                right.play()
                selected = [False, False, False, False, True]
                top_text[0] = font.render("Given these vitals, where does Grandpa seem hurt?", True, (0, 0, 0))
                phase = 4
            else:
                temp = 0
                for i in range(len(selected)):
                    if selected[i] != correct[i]:
                        temp += 1
                top_text[0] = font.render(f"{temp} of your selections are incorrect.", True, (0, 0, 0))
                wrong.play()
    elif phase == 4:
        if p2_button[0].click():
            phase = 0
            top_text[0] = font.render("Let's see what's wrong with Grandpa.", True, (0, 0, 0))
            right.play()
            return 4
        elif p2_button[1].click():
            top_text[0] = font.render(random.choice(hints), True, (0, 0, 0))
            wrong.play()
        elif p2_button[2].click():
            top_text[0] = font.render(random.choice(hints), True, (0, 0, 0))
            wrong.play()

    return 1

def draw():
    global phase
    if phase < 3:
        screen.blit(background[phase], screen.get_rect(topleft = (0, 0)))
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
        screen.blit(cont.display_image, cont.rect)
        database.blit_text(intro[2], screen)
    elif phase == 3 or phase == 4:
        screen.blit(background[2], screen.get_rect(topleft = (0, 0)))
        screen.blit(trans_back, screen.get_rect(topleft = (0, 0)))
        screen.blit(background[3], screen.get_rect(topleft = (0, 0)))

    if phase == 0:
        database.blit_text(intro[0], screen)
    elif phase == 2:
        pygame.draw.rect(screen, (255, 255, 255), intro[1][0].get_rect(topleft=intro[1][1]))
        database.blit_text(intro[1], screen)
    elif phase == 3:
        pygame.draw.rect(screen, (255, 255, 255), pygame.rect.Rect(50, 50, 1020, 130))
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(780, 15, 250, 110))
        for i in paper_text:
            database.blit_text(i, screen)
        for i in p1_button:
            screen.blit(i.display_image, i.rect)
        for i in table:
            pygame.draw.rect(screen, (0, 0, 0), i)
        for i in range(len(selected)):
            if selected[i]:
                screen.blit(confirm, p1_button[i].rect)
        database.blit_text(top_text, screen)
        database.blit_text(bot_text, screen)
        database.blit_text(sub_text, screen)
        screen.blit(pygame.image.load("assets/mark.png"), mark.get_rect(center=(180, 265)))
    elif phase == 4:
        pygame.draw.rect(screen, (255, 255, 255), pygame.rect.Rect(50, 50, 750, 65))
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(50, 95, 250, 110))
        pygame.draw.rect(screen, (0, 0, 30), pygame.rect.Rect(300, 95, 250, 110))
        pygame.draw.rect(screen, (30, 0, 0), pygame.rect.Rect(550, 95, 250, 110))
        for i in paper_text:
            database.blit_text(i, screen)
        for i in p2_text:
            database.blit_text(i, screen)
        for i in p2_button:
            screen.blit(i.display_image, i.rect)
        for i in table:
            pygame.draw.rect(screen, (0, 0, 0), i)
        database.blit_text(top_text, screen)