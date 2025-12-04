import pygame

pygame.init()


def blit_text(txt, screen):
    if txt[2]:
        rect = txt[0].get_rect(center=txt[1])
    else:
        rect = txt[0].get_rect(topleft=txt[1])
    screen.blit(txt[0], rect)

# button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img, click_img):
        super().__init__()
        self.display_image = img
        self.image = img
        self.clicked_image = click_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pressed = False

    def click(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and not self.pressed:
            self.pressed = True
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.display_image = self.clicked_image
        if not mouse[0] and self.pressed:
            self.pressed = False
            self.display_image = self.image
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False

class Timing(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/timing.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, delta):
        self.rect.centerx += delta * 200
