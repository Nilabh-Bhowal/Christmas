import pygame
import random
from assets.scripts.animation import Animation
from assets.scripts.blaster import Blaster
from assets.scripts.particle import ParticleEmitter

pygame.init()

hurt_sound = pygame.mixer.Sound("assets/sounds/effects/hurt.wav")

class Player:
    def __init__(self, x):
        self.rect = pygame.Rect(x, -110, 64, 64)
        self.y_momentum = 0
        self.x_momentum = 0
        self.movement = 0
        self.bottom_collision = False
        self.can_jump = False
        self.air_timer = 0
        self.platform_landed_on = None
        self.blaster = Blaster(self.rect.x, self.rect.y, self)
        self.death_particles = ParticleEmitter()
        self.move_particles = ParticleEmitter()
        self.animation = Animation("player")
        self.alive = True
        self.death_effect = True

    def update(self, platforms, dt):
        self.blaster.update(dt)
        self.y_momentum = min(self.y_momentum + 1 * dt, 20)
        self.rect.y += self.y_momentum * dt
        self.bottom_collision = False
        self.platform_landed_on = None
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.y_momentum >= 0 and platform.rect.bottom > self.rect.bottom - 5:
                self.platform_landed_on = platform
                self.rect.bottom = platform.rect.top + 1
                self.y_momentum = 0
                self.bottom_collision = True

        self.movement += self.x_momentum * dt
        self.movement *= 0.97
        self.rect.x += int(self.movement * dt)
        if self.rect.right < 0:
            self.rect.left = 720 * 9/16
        if self.rect.left > 720 * 9/16:
            self.rect.right = 0

        if self.bottom_collision:
            self.can_jump = True
            self.air_timer = 0
            if int(self.movement) > 0:
                for _ in range(5):
                    self.move_particles.add_particle(self.rect.left + random.randint(0, 48), self.rect.bottom, (230, 230, 255), 3 + random.randint(-50, 50) / 50, -1 + random.randint(-50, 50) / 50, 0.5, 3, 0.5)
            elif int (self.movement) < 0:
                for _ in range(5):
                    self.move_particles.add_particle(self.rect.right - random.randint(0, 48), self.rect.bottom, (230, 230, 255), 3 + random.randint(-50, 50) / 50, 1 + random.randint(-50, 50) / 50, 0.5, 3, 0.5)
        else:
            self.air_timer += 1
            if self.air_timer >= 10:
                self.can_jump = False

        if int(self.movement) > 0:
            self.animation.change_animation("right")
        elif int(self.movement) < 0:
            self.animation.change_animation("left")
        else:
            self.animation.change_animation("idle")

        if not self.alive and len(self.death_particles.particles) == 0:
            self.death_particles.add_burst(self.rect.centerx, self.rect.centery, (225, 225, 255), 10, 5, 0.25, 50)
            self.death_effect = False
            hurt_sound.play()
        self.death_particles.update(dt)
        self.move_particles.update(dt)

    def draw(self, screen, scroll):
        if self.alive:
            screen.blit(self.animation.get_image(), (self.rect.x, self.rect.y - scroll))
        self.blaster.draw(screen, scroll)
        self.death_particles.draw(screen, scroll)
        self.move_particles.draw(screen, scroll)
