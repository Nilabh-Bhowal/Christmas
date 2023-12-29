import pygame
from pygame.locals import *
import random
import time

from assets.scripts.player import Player
from assets.scripts.platforms import Platform, MovingPlatform, ShatterPlatform
from assets.scripts.boost import Boost
import assets.scripts.ui as ui
from assets.scripts.enemy import Enemy

pygame.init()

SCREEN_WIDTH = 720 * 9/16
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gift Blast")
pygame.display.set_icon(pygame.image.load("assets/images/icon.ico"))

ground_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/ground.png"))

small_still_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/still/small.png"))
medium_still_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/still/medium.png"))
large_still_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/still/large.png"))

small_moving_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/moving/small.png"))
medium_moving_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/moving/medium.png"))
large_moving_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/moving/large.png"))

small_cracked_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/cracked/small.png"))
medium_cracked_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/cracked/medium.png"))
large_cracked_platform = pygame.transform.scale2x(pygame.image.load("assets/images/platforms/cracked/large.png"))

enemy_img = pygame.transform.scale2x(pygame.image.load("assets/images/enemy.png"))

boost_img = pygame.transform.scale2x(pygame.image.load("assets/images/boost.png"))

boost_sound = pygame.mixer.Sound("assets/sounds/effects/boost.wav")
jump_sound = pygame.mixer.Sound("assets/sounds/effects/jump.wav")
jump_sound.set_volume(0.1)

pygame.mixer.music.load("assets/sounds/music/music.wav")
pygame.mixer.music.set_volume(0.1)

state = "main menu"

score = 0
high_score = 0

def generate_platform(platform_generation_height, platforms, boosts, enemies):
    for _ in range(random.randint(1, 10 - int(min(8, abs(platform_generation_height) / 10000)))):
        y = random.randint(platform_generation_height - 300, platform_generation_height - 150)
        width = random.randint(100, 200)
        width = random.randint(1, 3) * 64
        if width == 64:
            img = small_still_platform
        elif width == 128:
            img = medium_still_platform
        elif width == 192:
            img = large_still_platform
        x = random.randint(50, SCREEN_WIDTH - 50 - width)
        platforms.append(Platform(x, y, width, 20, img))
        if random.randint(1, 100) == 1:
            boosts.append(Boost(random.randint(x, x + width), y - 16, boost_img))

    if platform_generation_height < -7500:
        for _ in range(random.randint(1, 5 + int(min(10, abs(platform_generation_height) / 10000)))):
            y = random.randint(platform_generation_height - 300, platform_generation_height - 150)
            width = random.randint(100, 200)
            width = random.randint(1, 3) * 64
            if width == 64:
                img = small_moving_platform
            elif width == 128:
                img = medium_moving_platform
            elif width == 192:
                img = large_moving_platform
            x = random.randint(50, SCREEN_WIDTH - 50 - width)
            platforms.append(MovingPlatform(x, y, width, 20, img))

    if platform_generation_height < -7500:
        for _ in range(random.randint(1, 5 + int(min(10, abs(platform_generation_height) / 10000)))):
            y = random.randint(platform_generation_height - 300, platform_generation_height - 150)
            width = random.randint(100, 200)
            width = random.randint(1, 3) * 64
            if width == 64:
                img = small_cracked_platform
            elif width == 128:
                img = medium_cracked_platform
            elif width == 192:
                img = large_cracked_platform
            x = random.randint(50, SCREEN_WIDTH - 50 - width)
            platforms.append(ShatterPlatform(x, y, width, 20, img))
            if random.randint(1, 100) == 1:
                boosts.append(Boost(random.randint(x, x + width), y - 16, boost_img))

    if platform_generation_height < -10000:
        for _ in range(random.randint(0, 1 + int(abs(platform_generation_height) / 20000))):
            y = random.randint(platform_generation_height - 450, platform_generation_height - 150)
            random_num = random.randint(1, 2)
            x = random_num * 261 - 224
            if random_num == 1:
                direction = 1
            else:
                direction = -1
            enemies.append(Enemy(x, y, direction, enemy_img))
            if random.randint(1, 100) == 1:
                boosts.append(Boost(random.randint(x, x + width), y - 16, boost_img))

    for platform in platforms:
        if any((p.rect.colliderect(platform) or abs(p.rect.y - platform.rect.y) < 60) and p != platform and platforms.index(platform) != 0 for p in platforms):
            platforms.remove(platform)

    for enemy in enemies:
        if any((e.rect.colliderect(enemy)) and e != enemy for e in enemies):
            enemies.remove(enemy)

def main_menu(state):
    clock = pygame.time.Clock()

    play_button = ui.Button("Play", 200, 550, 128, 64, "menu_button")
    quit_button = ui.Button("Quit", 200, 650, 128, 64, "menu_button")

    while state == "main menu":
        for event in pygame.event.get():
            if event.type == QUIT:
                state = "quit"

        screen.fill((13, 29, 72))
        if play_button.draw(screen):
            state = "game"
        if quit_button.draw(screen):
            state = "quit"

        ui.title("Gift Blast", 200, 200, screen, (255, 255, 255))

        pygame.display.update()
        clock.tick(60)

    return state

def game_over(state, score, high_score):
    clock = pygame.time.Clock()

    play_button = ui.Button("Restart", 200, 550, 128, 64, "menu_button")
    quit_button = ui.Button("Quit", 200, 650, 128, 64, "menu_button")

    while state == "game over":
        for event in pygame.event.get():
            if event.type == QUIT:
                state = "quit"

        screen.fill((13, 29, 72))
        if play_button.draw(screen):
            state = "game"
        if quit_button.draw(screen):
            state = "quit"

        ui.title("Game Over", 200, 200, screen, (255, 255, 255))
        ui.heading(f"Score: {score}", 200, 275, screen, (255, 255, 255))
        ui.heading(f"High Score: {high_score}", 200, 300, screen, (255, 255, 255))

        pygame.display.update()
        clock.tick(60)

    return state

def main(state):
    clock = pygame.time.Clock()

    player = Player(SCREEN_WIDTH / 2 - 32)
    jumped = False

    scroll = 0

    platform_generation_height = 0
    platforms = [Platform(0, 0, SCREEN_WIDTH, 30, ground_platform)]
    boosts = []
    enemies = []

    enemies_zapped = 0

    lose_boundary = SCREEN_HEIGHT + 400

    score = 0

    pt = time.time()
    dt = 1

    pygame.mixer.music.play(-1)

    while state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "quit"

        key_pressed = pygame.key.get_pressed()
        player.x_momentum = key_pressed[K_RIGHT] - key_pressed[K_LEFT]
        if key_pressed[K_UP]:
            if player.can_jump and not jumped:
                jump_sound.play()
                player.y_momentum = -30
                for _ in range(50):
                    player.move_particles.add_particle(player.rect.centerx + random.randint(-32, 32), player.rect.bottom, (230, 230, 255), 5, random.randint(-50, 50) / 50, random.randint(0, 50) / 50, 3, 0.5)
            jumped = True
        else:
            jumped = False

        if key_pressed[K_SPACE]:
            player.blaster.fire_bullet()

        lose_boundary = min(lose_boundary, SCREEN_HEIGHT + 400 + scroll)

        player.update(platforms, dt)
        if player.rect.y > lose_boundary:
            player.alive = False
        for e in enemies:
            e.update(dt)
            for b in e.blaster.bullets:
                if b.rect.colliderect(player.rect) and not player.y_momentum < -30:
                    player.alive = False
            if e.rect.y > lose_boundary:
                enemies.remove(e)
        for e in enemies:
            for b in player.blaster.bullets:
                if b.rect.colliderect(e.rect):
                    player.blaster.bullets.remove(b)
                    e.alive = False
                    enemies_zapped += 1
            if e.death_effect == False and len(e.death_particles.particles) == 0:
                enemies.remove(e)
        if platform_generation_height > scroll - SCREEN_HEIGHT:
            generate_platform(platform_generation_height, platforms, boosts, enemies)
            platform_generation_height -= 300
        for platform in platforms:
            platform.update(dt, [player])
            if isinstance(platform, ShatterPlatform) and (platform.shatter_timer <= 0):
                platforms.remove(platform)
            if platform.rect.y > lose_boundary:
                platforms.remove(platform)

        if player.death_effect == False and len(player.death_particles.particles) == 0:
            state = "game over"

        for boost in boosts:
            boost.update(player)
            if boost.rect.y > lose_boundary:
                boosts.remove(boost)
            if boost.collected:
                boost_sound.play()
                boosts.remove(boost)
                player.y_momentum = -50

        scroll += ((player.rect.y - (SCREEN_HEIGHT / 2 - player.rect.height / 2) - scroll) / 2 * dt)
        scroll = int(scroll)
        scroll = min(scroll, -700)

        score = int(max(score, -player.rect.y / 10 - 9 + enemies_zapped * 100))

        screen.fill((13, 29, 72))
        for p in platforms:
            p.draw(screen, scroll)
        for b in boosts:
            b.draw(screen, scroll)
        for e in enemies:
            e.draw(screen, scroll)
        player.draw(screen, scroll)

        ui.heading(f"Score: {score}", int(720 * 9/32), 20, screen, (255, 255, 255))

        pygame.display.update()

        clock.tick(60)
        now = time.time()
        dt = (now - pt) * 60
        dt = min(dt, 4)
        pt = now

    pygame.mixer.music.fadeout(1000)
    return state, score


while state != "quit":
    if state == "main menu":
        state = main_menu(state)
    if state == "game":
        state, score = main(state)
        high_score = max(high_score, score)
    if state == "game over":
        state = game_over(state, score, high_score)

pygame.quit()
