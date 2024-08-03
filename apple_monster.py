import pygame
import random
import math
from pygame import time, image, mixer, font, Color

# initializing
pygame.init()
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
bg_image = image.load('background.jpg')
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
bg_image_rect = bg_image.get_rect()
bg_image_rect.topleft = (0, 0)

# monster object
monster = image.load('monster.png')
monster_x_scale, monster_y_scale = 30, 30
monster = pygame.transform.scale(monster, (monster_x_scale, monster_y_scale))
monster_rect = monster.get_rect()
monster_rect.topleft = (screen_width / 2, screen_height / 2)
monster_vel = 10

# apple object
apple = image.load('apple.png')
apple = pygame.transform.scale(apple, (20, 20))
apple_rect = apple.get_rect()
apple_rect.topleft = (
random.randint(0, screen_width - apple_rect.width), random.randint(41, screen_height - apple_rect.height))

# texts
level = 1
to_level_up = 3
required_apple = 3
apple_eaten = 0
game_font = font.SysFont('Arial', 20)
level_text = game_font.render(f"Level: {level}", True, (0, 0, 0))
level_text_rect = level_text.get_rect()
level_text_rect.topleft = (20, 10)
apple_text = game_font.render(f"Apples Eaten: {apple_eaten}", True, (0, 0, 0))
apple_text_rect = apple_text.get_rect()
apple_text_rect.topright = (580, 10)
win_font = font.SysFont('Arial', 50)
win_text = win_font.render("You Won!", True, (0, 0, 0))
win_text_rect = win_text.get_rect()
win_text_rect.center = (screen_width / 2, screen_height / 2)

# sounds
mixer.music.load('piano_background.wav')
mixer.music.play(-1, 0.0)
level_up_sound = mixer.Sound('jump.wav')

# game loop
fps = 30
clock = time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        monster_rect.y -= monster_vel
    elif keys[pygame.K_DOWN]:
        monster_rect.y += monster_vel
    elif keys[pygame.K_LEFT]:
        monster_rect.x -= monster_vel
    elif keys[pygame.K_RIGHT]:
        monster_rect.x += monster_vel

    monster_rect.x = max(0, min(monster_rect.x, screen_width - monster_rect.width))
    monster_rect.y = max(50, min(monster_rect.y, screen_height - monster_rect.height))

    screen.blit(bg_image, bg_image_rect)
    pygame.draw.rect(screen, Color("yellow"), (0, 0, 600, 40))
    screen.blit(level_text, level_text_rect)
    screen.blit(apple_text, apple_text_rect)
    screen.blit(apple, apple_rect)
    screen.blit(monster, monster_rect)

    if monster_rect.colliderect(apple_rect):
        apple_eaten += 1
        to_level_up -= 1
        apple_rect.topleft = (random.randint(0, screen_width - monster_rect.width), random.randint(41, screen_height - monster_rect.height))
        if to_level_up == 0:
            level += 1
            to_level_up = math.ceil(required_apple * 1.5)
            required_apple = to_level_up
            level_up_sound.play()
            monster_x_scale = monster_x_scale * 1.5
            monster_y_scale = monster_y_scale * 1.5
            monster_pos_x = monster_rect.x
            monster_pos_y = monster_rect.y
            monster = pygame.transform.scale(monster, (monster_x_scale, monster_y_scale))
            monster_rect = monster.get_rect()
            monster_rect.x = monster_pos_x
            monster_rect.y = monster_pos_y

            if monster_x_scale > 100 or monster_y_scale > 100:
                screen.blit(win_text, win_text_rect)
                pygame.display.update()
                time.delay(10000)
                running = False

        level_text = game_font.render(f"Level: {level}", True, (0, 0, 0))
        apple_text = game_font.render(f"Apples Eaten: {apple_eaten}", True, (0, 0, 0))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
