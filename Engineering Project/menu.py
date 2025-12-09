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

#creates button to start game
button = database.Button(100, 200, pygame.image.load("assets/button1.png"), pygame.image.load("assets/button2.png"))

#imports button click sound
click = pygame.mixer.Sound("assets/click.wav")

#list of text that will be blit on screen
text = [
    [
        #creates the text that will be rendered onto the screen
        font.render("EXPO PROJECT", True, (255, 255, 255)),
        #sets the position of the text
        (600, 50),
        #set whether text should be centered or set to top left
        True
    ],
    [
        font.render("Play Game", True, (255, 255, 255)),
        (200, 225),
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
        return 1

    #keeps gamestate to current state
    return 0

#per frame graphics
def draw():
    #refreshes the background with black every frame
    screen.fill("black")

    #draws all text onto screen
    for i in text:
        database.blit_text(i, screen)

    #draws button onto screen
    screen.blit(button.display_image, button.rect)
