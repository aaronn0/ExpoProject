"""
Modified: 8 December 2025
By Aaron Noh

Purpose: Provide several helper methods and classes used in other files
"""
import pygame

#initializes pygame
pygame.init()

#function to easily blit text onto screen
def blit_text(txt, screen):
    #checks if txt[2] is true
    if txt[2]:
        #if true, set a rect with size txt[0] with its CENTER point at txt[1]
        rect = txt[0].get_rect(center=txt[1])
    else:
        #if false, set a rect with size txt[0] with its TOP LEFT point at txt[1]
        rect = txt[0].get_rect(topleft=txt[1])

    #blit txt[0] at rect
    screen.blit(txt[0], rect)

# button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img, click_img):
        super().__init__()

        #display image is used when blitting, image and clicked image are stored to be used when the button is unclicked vs clicked respectively
        self.display_image = img
        self.image = img
        self.clicked_image = click_img

        #sets up button rect and places its position on screen
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #sets up pressed boolean
        self.pressed = False

    #checks whether player has clicked button and returns true/false
    def click(self):
        #gets current state of mouse
        mouse = pygame.mouse.get_pressed()

        #checks if left mouse button is pressed down and self.pressed is false
        if mouse[0] and not self.pressed:
            #sets self.pressed to true to make sure button only checks on first frame of the mouse being clicked
            self.pressed = True
            #if mouse is in the button rect, change current display image to clicked state
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.display_image = self.clicked_image

        #checks if left mouse button got let go after being pressed
        if not mouse[0] and self.pressed:
            self.pressed = False

            #returns display image to unclicked state
            self.display_image = self.image
            #checks if mouse is in the rect - if so return true
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        #return false in all other cases
        return False

#red timing class for phase 2
class Timing(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        #sets image to timing.png and sets its position to (x, y)
        self.image = pygame.image.load("assets/timing.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    #moves the timing class to the right every frame update is called
    def update(self, delta):
        self.rect.centerx += delta * 200
