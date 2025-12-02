#from machine import Pin

import pygame
#from machine import ADC, Pin, PWM
import time
import os
from datetime import datetime, date, timedelta

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


import database

#buttonPin = 14
#button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 800))

pygame.display.set_caption("ENGINEERING PROJECT")

clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont("Arial", 60)


class Game:
    def __init__(self):
        self.phase = 0
        self.delta = 0

        self.background = [
            pygame.image.load("assets/oldguynormal.jpg"),
            pygame.image.load("assets/heartattack.jpg"),
            pygame.image.load("assets/ground.jpg")
        ]

        for i in range(len(self.background)):
            self.background[i] = pygame.transform.scale(self.background[i], (1200, 800))

        self.intro = [
                font.render("This is Grandpa.", True, (0, 0, 0)),
                (80, 80),
                False
            ]
        self.text = [
            [
                font.render("Where do you think Grandpa got hurt?", True, (255, 255, 255)),
                (80, 80),
                False
            ],
            [
                font.render("Heart", True, (255, 255, 255)),
                (200, 195),
                False
            ],
            [
                font.render("Head", True, (255, 255, 255)),
                (200, 355),
                False
            ],
            [
                font.render("Arm", True, (255, 255, 255)),
                (200, 515),
                False
            ]
        ]

        self.button = [
            database.Button(120, 200, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png")),
            database.Button(120, 360, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png")),
            database.Button(120, 520, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png"))
        ]
        self.played = False

    def update(self, delta):
        if not self.played and self.phase == 0:
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/OST.wav"))
            self.played = True
        if self.delta < 9:
            self.delta += delta
        if 0 <= self.delta < 4:
            self.phase = 0
        elif 4 <= self.delta < 5:
            self.phase = 1
        elif 5 <= self.delta < 8:
            self.phase = 2
        elif 8 <= self.delta < 9:
            self.phase = 3

        if self.button[0].click():
            self.phase = 0
            self.delta = 0
            self.played = False
            return 3
        if self.button[1].click():
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/gta-ctw-wrong-buzzer-sound.wav"))
        if self.button[2].click():
            pygame.mixer.Sound.play(pygame.mixer.Sound("assets/gta-ctw-wrong-buzzer-sound.wav"))


        return 1

    def draw(self):
        if self.phase < 3:
            screen.blit(self.background[self.phase], screen.get_rect(topleft = (0, 0)))
        else:
            screen.fill("black")

        if self.phase == 0:
            if self.intro[2]:
                rect = self.intro[0].get_rect(center=self.intro[1])
            else:
                rect = self.intro[0].get_rect(topleft=self.intro[1])
            screen.blit(self.intro[0], rect)
        elif self.phase == 3:
            for i in self.text:
                if i[2]:
                    rect = i[0].get_rect(center=i[1])
                else:
                    rect = i[0].get_rect(topleft=i[1])
                screen.blit(i[0], rect)
            for i in self.button:
                screen.blit(i.display_image, i.rect)


class Difficulty:
    def __init__(self):
        self.select = pygame.image.load("assets/select.png")
        self.s_rect = self.select.get_rect(topleft = (110, 350))

        self.buttons = [
            database.Button(30, 30, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png")),
            database.Button(120, 200, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png")),
            database.Button(120, 360, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png")),
            database.Button(120, 520, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png")),
            database.Button(1100, 700, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png"))
        ]

        self.text = [
            [
                font.render("Set Difficulty", True, (255, 255, 255)),
                (600, 50),
                True
            ],
            [
                font.render("Easy", True, (255, 255, 255)),
                (200, 195),
                False
            ],
            [
                font.render("Medium", True, (255, 255, 255)),
                (200, 355),
                False
            ],
            [
                font.render("Hard", True, (255, 255, 255)),
                (200, 515),
                False
            ]
        ]

        self.difficulty = 2
        #background = pygame.image.load("assets/background.png")

    def update(self):
        if self.buttons[0].click():
            return 0
        if self.buttons[1].click():
            self.difficulty = 1
            self.s_rect.topleft = (110, 190)
        if self.buttons[2].click():
            self.difficulty = 2
            self.s_rect.topleft = (110, 350)
        if self.buttons[3].click():
            self.difficulty = 3
            self.s_rect.topleft = (110, 510)
        if self.buttons[4].click():
            return 2 + self.difficulty
        return 1

    def draw(self):
        screen.fill("black")

        screen.blit(self.select, self.s_rect)
        for i in self.buttons:
            screen.blit(i.display_image, i.rect)

        for i in self.text:
            if i[2]:
                rect = i[0].get_rect(center = i[1])
            else:
                rect = i[0].get_rect(topleft = i[1])
            screen.blit(i[0], rect)


class Learn:
    def __init__(self):
        self.testButton = database.Button(30, 30, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png"))

        self.font = pygame.font.SysFont("Arial", 40)

        self.text = [
            [
                font.render("ABOUT HEART PUMPS", True, (255, 255, 255)),
                (600, 50),
                True
            ],
            [
                self.font.render("="*50, True, (255, 255, 255)),
                (600, 120),
                True
            ],
            [
                self.font.render("A mechanical heart pump (also called a ventricular assist device) helps pump", True, (255, 255, 255)),
                (600, 190),
                True
            ],
            [
                self.font.render("blood when someone's heart is weak.", True, (255, 255, 255)),
                (600, 260),
                True
            ],
            [
                self.font.render("- Too SLOW: Not enough blood reaches the body", True, (255, 255, 255)),
                (600, 330),
                True
            ],
            [
                self.font.render("- Too FAST: Can damage blood cells and organs", True, (255, 255, 255)),
                (600, 400),
                True
            ],
            [
                self.font.render("That's why engineers test their designs many times!", True, (255, 255, 255)),
                (600, 470),
                True
            ],
            [
                self.font.render("="*50, True, (255, 255, 255)),
                (600, 540),
                True
            ]
        ]
        #background = pygame.image.load("assets/background.png")

        self.items = [self.testButton]

    def update(self):
        if self.testButton.click():
            return 0
        return 2

    def draw(self):
        screen.fill("black")
        for i in self.items:
            screen.blit(i.display_image, i.rect)

        for i in self.text:
            if i[2]:
                rect = i[0].get_rect(center = i[1])
            else:
                rect = i[0].get_rect(topleft = i[1])
            screen.blit(i[0], rect)


class MainMenu:
    def __init__(self):
        self.buttons = [
            database.Button(120, 200, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png")),
            database.Button(120, 500, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png")),
        ]

        self.text = [
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

    def update(self):
        if self.buttons[0].click():
            return 1
        if self.buttons[1].click():
            return 2
        return 0

    def draw(self):
        screen.fill("black")
        for i in self.text:
            if i[2]:
                rect = i[0].get_rect(center = i[1])
            else:
                rect = i[0].get_rect(topleft = i[1])
            screen.blit(i[0], rect)


        for i in self.buttons:
            screen.blit(i.display_image, i.rect)


class End():
    def __init__(self):
        self.button = database.Button(120, 360, pygame.image.load("assets/b_test_up.png"), pygame.image.load("assets/b_test_down.png"))

        self.text = [
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
    def update(self):
        if self.button.click():
            return 0
        return 3

    def draw(self):
        screen.fill("black")
        for i in self.text:
            if i[2]:
                rect = i[0].get_rect(center = i[1])
            else:
                rect = i[0].get_rect(topleft = i[1])
            screen.blit(i[0], rect)

        screen.blit(self.button.display_image, self.button.rect)


menu = MainMenu()
learn = Learn()
game = Game()
end = End()
num_states = 0

while running:
    dt = clock.tick(60) / 1000.0

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE
    if num_states == 0:
        num_states = menu.update()
        menu.draw()
    if num_states == 1:
        num_states = game.update(dt)
        game.draw()
    if num_states == 2:
        num_states = learn.update()
        learn.draw()
    if num_states == 3:
        num_states = end.update()
        end.draw()
    # flip() the display to put your work on screen
    pygame.display.flip()

      # limits FPS to 60

pygame.quit()

