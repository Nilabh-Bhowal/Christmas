import pygame

class Platform:
    def __init__(self, x, y, width, height, img):
        self.rect = pygame.Rect(x, y, width, height)
        self.img = img

    def update(self, dt, things):
        pass

    def draw(self, screen, scroll):
        screen.blit(self.img, (self.rect.x, self.rect.y - scroll))

class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.movement = 5

    def update(self, dt, things):
        super().update(dt, things)
        self.rect.x += self.movement * dt
        for thing in things:
            if thing.platform_landed_on == self:
                thing.rect.x += self.movement * dt

        if self.rect.right >= 720 * 9/16 - 50:
            self.movement = -5
        elif self.rect.left <= 50:
            self.movement = 5

class ShatterPlatform(Platform):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.shatter_timer = 15
        self.shatter = False

    def update(self, dt, things):
        super().update(dt, things)
        for thing in things:
            if thing.platform_landed_on == self:
                self.shatter = True

        if self.shatter:
            self.shatter_timer -= 1 * dt
