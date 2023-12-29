import pygame

pygame.init()

bullet_img = pygame.transform.scale2x(pygame.image.load("assets/images/bullet.png"))
shoot_sound = pygame.mixer.Sound("assets/sounds/effects/shoot.wav")
shoot_sound.set_volume(0.3)

class Blaster:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        self.direction = 1
        self.reload = 15
        self.bullets = []

    def fire_bullet(self):
        if self.reload <= 0:
            shoot_sound.play()
            self.bullets.append(Bullet(self.x, self.y, self.direction))
            self.reload = 15

    def update(self, dt):
        self.reload -= 1
        self.x = self.owner.rect.centerx
        self.y = self.owner.rect.centery
        if self.owner.movement < 0:
            self.direction = -1
        elif self.owner.movement > 0:
            self.direction = 1
        for b in self.bullets:
            b.update(dt)
            if b.deleted:
                self.bullets.remove(b)

    def draw(self, screen, scroll):
        for b in self.bullets:
            b.draw(screen, scroll)


class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 16, 16)
        self.direction = direction
        self.deleted = False

    def update(self, dt):
        self.rect.x += self.direction * 7 * dt
        if self.rect.right > 405 or self.rect.left < 0:
            self.deleted = True

    def draw(self, screen, scroll):
        screen.blit(bullet_img, (self.rect.x, self.rect.y - scroll))
