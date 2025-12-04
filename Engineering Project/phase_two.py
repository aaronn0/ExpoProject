import pygame
import os
import belay
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

device = belay.Device("COM5")

import database

pygame.init()
screen = pygame.display.set_mode((1200, 800))

font = pygame.font.Font("assets/font.ttf", 25)
bigfont = pygame.font.Font("assets/font.ttf", 75)

phase = 0

failed = 0
health = 0
started = False

pumping = False
pumptime = 0

interval = 0.5
countdown = 3
target = random.random()

dial1 = pygame.image.load("assets/dial.png")
dial2 = pygame.image.load("assets/dial.png")

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
            font.render(f"{health}/35 successful compressions.", True, (0, 200, 100)),
            (50, 110),
            False
        ],
        [
            font.render("(Failing 7 compressions makes you lose!)", True, (0, 0, 0)),
            (50, 170),
            False
        ]
    ],
    [
        [
            font.render("Well done! Grandpa should have a stable heartrate!", True, (0, 0, 0)),
            (50, 50),
            False
        ],
        [
            font.render("Unfortunately, the heart pump still seems faulty.", True, (0, 0, 0)),
            (50, 110),
            False
        ],
        [
            font.render("If a heart pump is too slow, not enough blood reaches the body.", True, (0, 0, 100)),
            (50, 210),
            False
        ],
        [
            font.render("Too fast, and the pump can damage blood cells and organs.", True, (0, 100, 0)),
            (50, 310),
            False
        ],
        [
            font.render("Normally engineers have to test their designs to ensure this doesn't happen.", True, (0, 0, 0)),
            (50, 410),
            False
        ]
    ],
    [
        [
            font.render("Luckily for us, we should be able to fix this ourselves!", True, (0, 0, 0)),
            (50, 50),
            False
        ],
        [
            font.render("Use the potentiometer below to tune the speed of the pump.", True, (0, 0, 0)),
            (50, 110),
            False
        ],
        [
            font.render("Match both dials to tune the pump.", True, (0, 0, 0)),
            (50, 160),
            False
        ],
        [
            bigfont.render(f"{int(countdown + 1)}", True, (255, 255, 255)),
            (600, 400),
            True
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

pressed = False

@device.task
def button_value():
    from machine import Pin, ADC
    # Set up button pin as an input
    buttonPin = 14
    button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)
    return button.value()

@device.task
def start_pump():
    from machine import Pin, ADC
    # Set up heartbeat signal pin (motor)
    sig = Pin(15, Pin.OUT)

    sig.value(1)

@device.task
def end_pump():
    from machine import Pin, ADC
    # Set up heartbeat signal pin (motor)
    sig = Pin(15, Pin.OUT)

    sig.value(0)

@device.task
def pot_value():
    from machine import Pin, ADC
    # Set up potentiometer
    pot = ADC(26)  # middle pin of potentiometer connected to GP26
    # Read potentiometer (0–65535)
    pot_value = pot.read_u16()

    # Calculate percentage (0-100%)
    pot_percent = pot_value / 65535
    return pot_percent

def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)

def update(delta):
    global phase, wait, timings, started, health, failed, pressed, pumping, pumptime, countdown, target

    if pumping:
        pumptime += delta
        if pumptime > 0.1:
            pumptime = 0
            pumping = False
            end_pump()

    if phase < 3:
        if cont.click():
            phase += 1
            click.play()
            if phase == 2:
                cont.rect = cont.rect.move((0, -340))
                intro[0][1] = (160, 350)
                intro[0][0] = font.render("Start", True, (0, 200, 0))
    elif phase == 3:
        latest_command = button_value()
        wait += delta

        if wait >= 0.5:
            wait = 0
            timings.append(database.Timing(-50, 532))
            if not started:
                started = True

        if started:

            if len(timings) > 0:
                if latest_command == 0 and not pressed:
                    if 754 < timings[0].rect.centerx < 846:
                        start_pump()
                        pumping = True
                        health += 1
                    else:
                        failed += 1
                    timings.pop(0)
                    pressed = True
                elif latest_command == 1 and pressed:
                    pressed = False
                elif timings[0].rect.centerx >= 846:
                    failed += 1
                    timings.pop(0)

            if health >= 35 or failed >= 7:
                if health >= 35:
                    cont.rect = cont.rect.move((0, 340))
                    intro[0][1] = (160, 690)
                    intro[0][0] = font.render("Continue", True, (0, 200, 0))
                    phase += 1
                    intro[3][0] = [
                        font.render("For now, let's try to keep Grandpa stable by performing CPR on him.", True, (255, 0, 0)),
                        (50, 50),
                        False
                    ]
                elif failed >= 7:
                    phase = 2
                    intro[3][0] = [
                        font.render("", True, (255, 0, 0)),
                        (50, 50),
                        False
                    ]
                timings = []
                wait = 0
                started = False
                failed = 0
                health = 0

            intro[4][0] = [
                font.render(f"{failed}/7 failed compressions.", True, (255, 0, 0)),
                (50, 50),
                False
            ]
            intro[4][1] = [
                font.render(f"{health}/35 successful compressions.", True, (0, 200, 100)),
                (50, 110),
                False
            ]

            for t in timings:
                t.update(delta)
    elif phase == 4:
        wait += delta
        if wait > (0.5 * (pot_value()/target)):
            pumping = True
            start_pump()
            wait = 0
        if cont.click():
            phase += 1
            click.play()
    elif phase == 5:
        wait += delta
        if wait > (0.5 * (pot_value()/target)):
            pumping = True
            start_pump()
            wait = 0

        if target - 0.05 < pot_value() < target + 0.05:
            countdown -= delta
            intro[6][3] =  [
                bigfont.render(f"{int(countdown + 1)}", True, (0, 100, 200)),
                (600, 400),
                True
            ]
        else:
            countdown = 3
            intro[6][3] =  [
                bigfont.render(f"{int(countdown + 1)}", True, (255, 255, 255)),
                (600, 400),
                True
            ]

        if countdown < 0:
            phase = 0
            wait = 0
            target = random.random()
            countdown = 3
            intro[6][3] =  [
                bigfont.render(f"{int(countdown + 1)}", True, (255, 255, 255)),
                (600, 400),
                True
            ]
            end_pump()
            return 3



    return 4

def draw():
    global phase
    if phase < 2:
        screen.blit(background[0], screen.get_rect(topleft=(0, 0)))
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
        screen.blit(cont.display_image, cont.rect)
        database.blit_text(intro[0], screen)
    elif phase == 2 or phase == 3:
        screen.fill((255, 255, 255))

        screen.blit(barmid, barmid.get_rect(topleft = (0, 500)))
        screen.blit(barend, barend.get_rect(topleft = (900, 500)))

        for tim in timings:
            screen.blit(tim.image, tim.rect)

        screen.blit(heart[health//6], heart[health//6].get_rect(center = (1070, 532)))

        screen.blit(selection, selection.get_rect(center = (800, 532)))
        screen.blit(container, container.get_rect(center = (800, 532)))

        if phase == 2:
            pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 300, 320, 110))
            screen.blit(cont.display_image, cont.rect)
            database.blit_text(intro[0], screen)
    elif phase == 4:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
        screen.blit(cont.display_image, cont.rect)
        database.blit_text(intro[0], screen)
    elif phase == 5:
        screen.fill((255, 255, 255))
        blitRotateCenter(screen, dial1, (204, 504), pot_value() * 360)
        blitRotateCenter(screen, dial2, (804, 504), target * 360)

    for t in intro[phase + 1]:
        database.blit_text(t, screen)