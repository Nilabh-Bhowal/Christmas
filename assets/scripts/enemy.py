import pygame
from assets.scripts.blaster import Blaster
from assets.scripts.particle import ParticleEmitter

class Enemy:
    def __init__(self, x, y, direction, img):
        self.rect = pygame.Rect(x, y, 64, 64)
        self.blaster = Blaster(self.rect.x, self.rect.y, self)
        self.alive = True
        self.movement = direction
        self.blaster.direction = direction
        self.shoot_timer = 60
        self.death_particles = ParticleEmitter()
        self.death_effect = True
        if direction == 1:
            self.img = img
        else:
            self.img = pygame.transform.flip(img, True, False)

    def update(self, dt):
        if self.alive:
            self.shoot_timer -= 1 * dt
            if self.shoot_timer <= 0:
                self.shoot_timer = 60
                self.blaster.reload = 0
                self.blaster.fire_bullet()

        if not self.alive and len(self.death_particles.particles) == 0:
            self.death_particles.add_burst(self.rect.centerx, self.rect.centery, (225, 225, 255), 10, 5, 0.5, 50)
            self.death_effect = False
            self.blaster.bullets = []
        self.blaster.update(dt)
        self.death_particles.update(dt)

    def draw(self, screen, scroll):
        if self.alive:
            screen.blit(self.img, (self.rect.x, self.rect.y - scroll))
        self.death_particles.draw(screen, scroll)
        self.blaster.draw(screen, scroll)
