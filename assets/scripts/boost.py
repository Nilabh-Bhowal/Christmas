import pygame

class Boost:
    def __init__(self, x, y, img):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.collected = False
        self.img = img

    def update(self, player):
        if player.rect.colliderect(self.rect):
            self.collected = True

    def draw(self, screen, scroll):
        screen.blit(self.img, (self.rect.x, self.rect.y - scroll))
