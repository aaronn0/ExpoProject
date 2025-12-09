"""
Modified: 8 December 2025
By Aaron Noh

Purpose: Teach the player about heart pumps, have them play a game where they perform CPR on a patient, and let them "retune a heart pump" by using a potentiometer.
"""
import pygame
import os
import belay
import random

#sets current working directory to current file folder, allows this file to be run even if moving from computer to computer
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#sets device to the pico kit connected to port COM5 (change this if your port is different)
device = belay.Device("COM5")

#imports database to use classes inside
import database

#pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 800))

#create text font to use for print on screen
font = pygame.font.Font("assets/font.ttf", 25)
bigfont = pygame.font.Font("assets/font.ttf", 75)

#create background
background = pygame.image.load("assets/heartpump.jpg")

#scale background to size of screen
background = pygame.transform.scale(background, screen.get_size())

#set phase variable to track which part player is on
phase = 0

#health and failed variable for CPR portion
failed = 0
health = 0

#countdown for how long potentiometer is the same as target
countdown = 3

#list of text that will be blit on screen
text = [
    [
        # creates the text that will be rendered onto the screen
        font.render("Continue", True, (0, 200, 0)),
        # sets the position of the text
        (160, 690),
        # set whether text should be centered or set to top left
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

#continue button during intro portion
cont = database.Button(50, 650, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

#variable to track whether to start the motor and the length of time motor has been activated for
pumping = False
pumptime = 0


#variable to track whether CPR game has started
started = False

#create list of heart states, from grey to bright red
heart = []
for i in range(6):
    heart.append(pygame.image.load(f"assets/heart{i + 1}.png"))

#variable to help track whether the CPR button has been pressed on the first frame
pressed = False

#images for the background bar behind the timings
barend = pygame.image.load("assets/barend.png")
barmid = pygame.image.load("assets/barmid.png")

#stretches barmid to desired length
barmid = pygame.transform.scale(barmid, (900, 64))

#creates semi-transparent rectangle to show correct range
selection = pygame.surface.Surface((60, 400), pygame.SRCALPHA)
selection.fill((0, 100, 100, 100))

#image of outline for selection rectangle
container = pygame.image.load("assets/selectcontainer.png")

#list of timing variables
timings = []
wait = 0

#target interval to hit for potentiometer section
target = random.random() * 0.8 + 0.1

#2 images for dials, one for the target position, other for the potentiometer
dial1 = pygame.image.load("assets/dial.png")
dial2 = pygame.image.load("assets/dial.png")

#load sound effects
click = pygame.mixer.Sound("assets/click.wav")
beat = pygame.mixer.Sound("assets/beat.wav")

@device.task
def button_value():
    from machine import Pin, ADC
    # Set up button pin as an input
    buttonPin = 14
    button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)

    #returns current button value
    return button.value()

@device.task
def start_pump():
    from machine import Pin, ADC
    # Set up heartbeat signal pin (motor)
    sig = Pin(15, Pin.OUT)

    #activates motor
    sig.value(1)

@device.task
def end_pump():
    from machine import Pin, ADC
    # Set up heartbeat signal pin (motor)
    sig = Pin(15, Pin.OUT)

    #stops motor
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

    #return percentage
    return pot_percent

#function to blit an object at a certain rotation while keeping it centered
def blitRotateCenter(surf, image, topleft, angle):
    #rotates image based on angle
    rotated_image = pygame.transform.rotate(image, angle)

    #sets center of the image to the correct position
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    #blits the image to the screen
    surf.blit(rotated_image, new_rect)

#per frame logic
def update(delta):
    global phase, wait, timings, started, health, failed, pressed, pumping, pumptime, countdown, target

    #starts tracking how much time has passed since pumping is true, stops once pumptime > 0.1 and stops the motor
    if pumping:
        pumptime += delta
        if pumptime > 0.1:
            pumptime = 0
            pumping = False
            end_pump()

    #logic if phase is less than 3
    if phase < 3:
        #increases phase by 1 if the continue button is pressed
        if cont.click():
            phase += 1
            click.play()

            #moves and renames continue button to "Start" when phase is equal to 2
            if phase == 2:
                cont.rect = cont.rect.move((0, -340))
                text[0][1] = (160, 350)
                text[0][0] = font.render("Start", True, (0, 200, 0))

    #logic if phase is equal to 3, CPR portion
    elif phase == 3:
        #gets current state of the physical button
        latest_command = button_value()
        #increases wait by delta
        wait += delta

        #resets wait to 0 if it is above 0.5 and spawns a Timing object, sets start to true if it is false
        if wait >= 0.5:
            wait = 0
            timings.append(database.Timing(-50, 532))
            if not started:
                started = True


        #logic for when CPR portion starts
        if started:
            #checks if timings has items inside
            if len(timings) > 0:
                #checks if the CPR button was pressed
                if latest_command == 0 and not pressed:
                    #destroys the item in timings[0], if it is inside the correct range it adds 1 to health and starts motor
                    if 754 < timings[0].rect.centerx < 846:
                        start_pump()
                        beat.play()
                        pumping = True
                        health += 1
                        #update onscreen text to reflect changes
                        text[4][1] = [
                            font.render(f"{health}/35 successful compressions.", True, (0, 200, 100)),
                            (50, 110),
                            False
                        ]
                    #otherwise add 1 to failed
                    else:
                        failed += 1
                        #update onscreen text to reflect changes
                        text[4][0] = [
                            font.render(f"{failed}/7 failed compressions.", True, (255, 0, 0)),
                            (50, 50),
                            False
                        ]
                    timings.pop(0)
                    pressed = True
                #checks if CPR button was let go
                elif latest_command == 1 and pressed:
                    pressed = False
                #checks if the oldest timing item is past 846, if so destroys it and adds 1 to failed
                elif timings[0].rect.centerx >= 846:
                    failed += 1
                    #update onscreen text to reflect changes
                    text[4][0] = [
                        font.render(f"{failed}/7 failed compressions.", True, (255, 0, 0)),
                        (50, 50),
                        False
                    ]
                    timings.pop(0)

            #checks if either health >= 35 or failed >= 7, if so reset all variables
            if health >= 35 or failed >= 7:
                #if health > 35, reset text variables, continue button, and add 1 to phase
                if health >= 35:
                    cont.rect = cont.rect.move((0, 340))
                    text[0][1] = (160, 690)
                    text[0][0] = font.render("Continue", True, (0, 200, 0))
                    phase += 1
                    text[3][0] = [
                        font.render("For now, let's try to keep Grandpa stable by performing CPR on him.", True, (0, 0, 0)),
                        (50, 50),
                        False
                    ]
                #otherwise set phase back to 2
                elif failed >= 7:
                    phase = 2
                    text[3][0] = [
                        font.render("", True, (255, 0, 0)),
                        (50, 50),
                        False
                    ]
                timings = []
                wait = 0
                started = False
                failed = 0
                health = 0
                text[4][0] = [
                    font.render(f"{failed}/7 failed compressions.", True, (255, 0, 0)),
                    (50, 50),
                    False
                ]
                text[4][1] = [
                    font.render(f"{health}/35 successful compressions.", True, (0, 200, 100)),
                    (50, 110),
                    False
                ]

            #calls update function of all items in timings
            for t in timings:
                t.update(delta)

    #logic for when phase is equal to 4
    elif phase == 4:
        #add delta to wait every frame
        wait += delta

        #starts heart pump function based on difference in pot_value() and target
        if wait > (0.5 * (pot_value()/target)):
            pumping = True
            start_pump()
            beat.play()
            wait = 0

        #increases phase by 1 if the continue button is pressed
        if cont.click():
            while pot_value() - 0.2 < target < pot_value() + 0.2:
                target = random.random() * 0.8 + 0.1
            phase += 1
            click.play()

    #logic for when phase is equal to 5
    elif phase == 5:
        #add delta to wait every frame
        wait += delta

        #starts heart pump function based on difference in pot_value() and target
        if wait > (0.5 * (pot_value()/target)):
            pumping = True
            beat.play()
            start_pump()
            wait = 0

        #if the pot value is within 0.05 of the target, starts countdown to ending
        if target - 0.05 < pot_value() < target + 0.05:
            #subtracts countdown by delta
            countdown -= delta

            #updates text to reflect changes
            text[6][3] =  [
                bigfont.render(f"{int(countdown + 1)}", True, (0, 100, 200)),
                (600, 400),
                True
            ]
        #otherwise reset countdown to 3 and update text
        else:
            countdown = 3
            text[6][3] =  [
                bigfont.render(f"{int(countdown + 1)}", True, (255, 255, 255)),
                (600, 400),
                True
            ]

        #if countdown reaches zero, reset all variables and set the overall gamestate to end
        if countdown < 0:
            phase = 0
            wait = 0
            while pot_value() - 0.2 < target < pot_value() + 0.2:
                target = random.random() * 0.8 + 0.1
            countdown = 3
            text[6][3] =  [
                bigfont.render(f"{int(countdown + 1)}", True, (255, 255, 255)),
                (600, 400),
                True
            ]
            end_pump()
            return 3

    #keeps gamestate to current state
    return 2

#per frame graphics
def draw():
    global phase
    #graphics if phase is less than 2
    if phase < 2:
        #draws background corresponding to current phase
        screen.blit(background, screen.get_rect(topleft=(0, 0)))

        #draws continue button
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
        screen.blit(cont.display_image, cont.rect)
        database.blit_text(text[0], screen)

    #graphics if phase is equal to 2 or 3
    elif phase == 2 or phase == 3:
        #refreshes background with white every frame
        screen.fill((255, 255, 255))

        #draws gray bar
        screen.blit(barmid, barmid.get_rect(topleft = (0, 500)))
        screen.blit(barend, barend.get_rect(topleft = (900, 500)))

        #draws all items within timings
        for tim in timings:
            screen.blit(tim.image, tim.rect)

        #draws the current heart state based on health
        screen.blit(heart[health//6], heart[health//6].get_rect(center = (1070, 532)))

        #draws the selection bar to know when to click CPR button
        screen.blit(selection, selection.get_rect(center = (800, 532)))
        screen.blit(container, container.get_rect(center = (800, 532)))

        #draws start button if phase is equal to 2
        if phase == 2:
            pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 300, 320, 110))
            screen.blit(cont.display_image, cont.rect)
            database.blit_text(text[0], screen)

    #graphics if phase is equal to 4
    elif phase == 4:
        #refreshes background with white every frame
        screen.fill((255, 255, 255))

        #draws continue button
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
        screen.blit(cont.display_image, cont.rect)
        database.blit_text(text[0], screen)

    #graphics if phase is equal to 5
    elif phase == 5:
        #refreshes background with white every frame
        screen.fill((255, 255, 255))

        #draws dials and rotates them based on their target value and potentiometer value
        blitRotateCenter(screen, dial1, (204, 504), pot_value() * 360)
        blitRotateCenter(screen, dial2, (804, 504), target * 360)

    #draws text based on current phase
    for t in text[phase + 1]:
        database.blit_text(t, screen)