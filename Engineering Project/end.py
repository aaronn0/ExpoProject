import pygame
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

#creates button to return player to menu
button = database.Button(50, 650, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

#imports button click sound
click = pygame.mixer.Sound("assets/click.wav")

#imports background image and scales it to screen size
background = pygame.image.load("assets/happy.jpg")
background = pygame.transform.scale(background, screen.get_size())

#list of text that will be blit on screen
text = [
    [
        #creates the text that will be rendered onto the screen
        font.render("Great job! You were able to save Grandpa!!", True, (0, 0, 0)),
        #sets the position of the text
        (600, 50),
        #set whether text should be centered or set to top left
        True
    ],
    [
        font.render("Thank you for playing!", True, (0, 0, 0)),
        (600, 120),
        True
    ],
    [
        font.render("Main Menu", True, (0, 200, 0)),
        (160, 690),
        False
    ]
]

#per frame logic
def update():
    #checks if end button is clicked
    if button.click():
        #plays click sound
        click.play()
        #sets gamestate to menu
        return 0

    #keeps gamestate to current state
    return 3

#per frame graphics
def draw():
    #draws background onto screen
    screen.blit(background, (0, 0))
    #draws a rect for the end button to be more visually appealing
    pygame.draw.rect(screen, (0, 30, 0), pygame.rect.Rect(40, 640, 320, 110))

    #draws all text onto screen
    for i in text:
        database.blit_text(i, screen)

    #draws button onto screen
    screen.blit(button.display_image, button.rect)