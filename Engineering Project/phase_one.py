import pygame
import random
import os

#sets current working directory to current file folder, allows this file to be run even if moving from computer to computer
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#imports database to use classes inside
import database

#pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 800))

#create text font to use for print on screen
font = pygame.font.Font("assets/font.ttf", 25)

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

#create a semi-transparent black layer
trans_back = pygame.surface.Surface(screen.get_size(), pygame.SRCALPHA)
trans_back.fill((0, 0, 0, 125))

#set phase variable to track which part player is on
phase = 0

#list of text that will be blit on screen, only for intro portion
intro = [
    [
        # creates the text that will be rendered onto the screen
        font.render("This is Grandpa.", True, (0, 0, 0)),
        # sets the position of the text
        (80, 80),
        # set whether text should be centered or set to top left
        False
    ],
    [
        font.render("Oh No! Grandpa's Collapsed!", True, (0, 0, 0)),
        (80, 80),
        False
    ],
    [
        font.render("Continue", True, (0, 200, 0)),
        (160, 690),
        False
    ]

]

#continue button during intro portion
cont = database.Button(50, 650, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

#list of text that will be blit on screen, only for the paper chart
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

#text that will be blit on screen, top portion
top_text = [
    font.render("Let's see what's wrong with Grandpa.", True, (0, 0, 0)),
    (50, 70),
    False
]

#text that will be blit on screen, bottom portion
bot_text = [
    font.render("Compare each set of vitals and mark down if they are different.", True, (0, 0, 0)),
    (50, 140),
    False
]

#submit text for button
sub_text = [
        font.render("Submit", True, (0, 200, 0)),
        (820, 60),
        False
    ]

#list of rectangles used to create the table on the paper chart
table = [
    pygame.rect.Rect(690, 220, 5, 570),
    pygame.rect.Rect(430, 220, 5, 570),
    pygame.rect.Rect(240, 290, 730, 5),
    pygame.rect.Rect(240, 410, 730, 5),
    pygame.rect.Rect(240, 510, 730, 5),
    pygame.rect.Rect(240, 610, 730, 5),
    pygame.rect.Rect(240, 700, 730, 5),
]

#list of buttons used during part 1 of the paper chart diagnosis
part1_button = [
    database.Button(130, 320, pygame.image.load("assets/select1.png"), pygame.image.load("assets/select1.png")),
    database.Button(130, 430, pygame.image.load("assets/select2.png"), pygame.image.load("assets/select2.png")),
    database.Button(130, 520, pygame.image.load("assets/select1.png"), pygame.image.load("assets/select1.png")),
    database.Button(130, 625, pygame.image.load("assets/select3.png"), pygame.image.load("assets/select3.png")),
    database.Button(130, 720, pygame.image.load("assets/select2.png"), pygame.image.load("assets/select2.png")),
    database.Button(930, 25, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))
]

#list of selected options for part 1 of paper diagnosis
selected = [False, False, False, False, True]
#list of correct options for part 1 of paper diagnosis
correct = [False, True, True, True, True]

#confirm image used during part 1 of paper chart diagnosis, corresponds with selected buttons in part 1
confirm = pygame.image.load("assets/confirm.png")
#text directing player to mark the buttons on left side for part 1
mark = pygame.image.load("assets/mark.png")

#list of buttons used during part 2 of the paper chart diagnosis
part2_button = [
    database.Button(60, 105, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png")),
    database.Button(310, 105, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png")),
    database.Button(560, 105, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))
]

#corresponding text used during part 2 of the paper chart diagnosis
part2_text = [
    [
        font.render("Heart", True, (0, 200, 0)),
        (170, 145),
        False
    ],
    [
        font.render("Legs", True, (20, 80, 230)),
        (430, 145),
        False
    ],
    [
        font.render("Head", True, (200, 0, 0)),
        (670, 145),
        False
    ]
]

#hints if player gets answer wrong in part 2 of paper chart diagnosis
hints = [
    "Maybe look at his heartrate?",
    "His heartrate seems strangely low..."
]

#sounds used throughout game
wrong = pygame.mixer.Sound("assets/wrong.wav")
write = pygame.mixer.Sound("assets/write.wav")
right = pygame.mixer.Sound("assets/right.wav")
click = pygame.mixer.Sound("assets/click.wav")

#per frame logic
def update():
    global phase, selected
    #makes continue button increase phase if clicked while phase is less than 3
    if phase < 3:
        if cont.click():
            click.play()
            phase += 1

    #logic if phase is equal to 3, part 1 of paper diagnosis starts
    elif phase == 3:
        #logic for all part1 buttons other than part1_button[5], if they are clicked changes corresponding selected variable and plays write sound
        for i in range(len(selected)):
            if part1_button[i].click():
                write.play()
                selected[i] = not selected[i]

        #logic for part1_button[5], compares selected with correct to see if player has the correct diagnosis
        if part1_button[5].click():
            #if player is correct, resets previous variables and sets current phase to 4
            if selected == correct:
                right.play()
                selected = [False, False, False, False, True]
                top_text[0] = font.render("Given these vitals, where does Grandpa seem hurt?", True, (0, 0, 0))
                phase = 4

            #otherwise give a hint on what is wrong
            else:
                temp = 0
                for i in range(len(selected)):
                    if selected[i] != correct[i]:
                        temp += 1
                top_text[0] = font.render(f"{temp} of your selections are incorrect.", True, (0, 0, 0))
                wrong.play()

    #logic if phase is equal to 4, part 2 of paper diagnosis starts, quizzes player on what exactly is wrong with Grandpa
    elif phase == 4:
        #logic for correct answer, resets previous variables and sets overall gamestate to phase 2
        if part2_button[0].click():
            phase = 0
            top_text[0] = font.render("Let's see what's wrong with Grandpa.", True, (0, 0, 0))
            right.play()
            return 2
        #logic for incorrect answer, plays wrong sound effect and creates a random hint for player
        elif part2_button[1].click() or part2_button[2].click():
            top_text[0] = font.render(random.choice(hints), True, (0, 0, 0))
            wrong.play()

    #keeps gamestate to current state
    return 1

#per frame graphics
def draw():
    global phase
    #graphics if phase is less than 3
    if phase < 3:
        #draws background corresponding to current phase
        screen.blit(background[phase], screen.get_rect(topleft = (0, 0)))

        #draws continue button
        pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))
        screen.blit(cont.display_image, cont.rect)
        database.blit_text(intro[2], screen)

        #draws text corresponding to current phase
        if phase == 0:
            database.blit_text(intro[0], screen)
        elif phase == 2:
            #draws white rectangle for visibility
            pygame.draw.rect(screen, (255, 255, 255), intro[1][0].get_rect(topleft=intro[1][1]))
            database.blit_text(intro[1], screen)

    #graphics if phase is equal to 3 or 4
    elif phase == 3 or phase == 4:
        #draws background corresponding to current phase
        screen.blit(background[2], screen.get_rect(topleft = (0, 0)))
        screen.blit(trans_back, screen.get_rect(topleft = (0, 0)))
        screen.blit(background[3], screen.get_rect(topleft = (0, 0)))

        #specific graphics for phase 3
        if phase == 3:
            #draws rectangles for visibility and asthetics
            pygame.draw.rect(screen, (255, 255, 255), pygame.rect.Rect(50, 50, 1020, 130))
            pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(780, 15, 250, 110))

            #draws all text onto paper chart
            for i in paper_text:
                database.blit_text(i, screen)

            #draws all buttons
            for i in part1_button:
                screen.blit(i.display_image, i.rect)

            #draws all black lines from table onto paper chart
            for i in table:
                pygame.draw.rect(screen, (0, 0, 0), i)

            #draws a red X corresponding to selected
            for i in range(len(selected)):
                if selected[i]:
                    screen.blit(confirm, part1_button[i].rect)

            #draws top text, bottom text, and submit text
            database.blit_text(top_text, screen)
            database.blit_text(bot_text, screen)
            database.blit_text(sub_text, screen)

            #draws "Mark Here" text
            screen.blit(pygame.image.load("assets/mark.png"), mark.get_rect(center=(180, 265)))

        #specific graphics for phase 4
        elif phase == 4:
            #draws rectangles for visibility and asthetics
            pygame.draw.rect(screen, (255, 255, 255), pygame.rect.Rect(50, 50, 750, 65))
            pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(50, 95, 250, 110))
            pygame.draw.rect(screen, (0, 0, 30), pygame.rect.Rect(300, 95, 250, 110))
            pygame.draw.rect(screen, (30, 0, 0), pygame.rect.Rect(550, 95, 250, 110))

            #draws all text onto paper chart
            for i in paper_text:
                database.blit_text(i, screen)

            #draws buttons for quiz
            for i in part2_button:
                screen.blit(i.display_image, i.rect)

            #draws text corresponding with buttons
            for i in part2_text:
                database.blit_text(i, screen)

            #draws all black lines from table onto paper chart
            for i in table:
                pygame.draw.rect(screen, (0, 0, 0), i)

            #draws top text
            database.blit_text(top_text, screen)