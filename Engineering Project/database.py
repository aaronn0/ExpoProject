import pygame

pygame.init()

# button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img, click_img, toggle = False):
        super().__init__()
        self.display_image = img
        self.image = img
        self.clicked_image = click_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pressed = False
        self.toggle = toggle

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