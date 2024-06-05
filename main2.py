import pygame
import sys
import math
from wheel import Wheel
from backdrop import Backdrop
from powerups import Powerups
import config
import os

os.makedirs('screenshots', exist_ok=True)

window_width = config.window_width
window_height = config.window_height
ground_height = config.ground_height

max_health = 500

powerups_to_draw = []
powerup_on_screen = False
add_powerup = True


def reset_players():
    player1.set(0, window_height - ground_height)

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
caption = pygame.display.set_caption("Deppecyloid")
pygame.mouse.set_visible(False)
font_small = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 100)


backdrop = Backdrop("blue_sky")

player1 = Wheel("Bike")

# player2 = Wheel("BeachBall")

reset_players()


frame_count = 0
while True:

    
    window.blit(backdrop.backdrop, (0, 0))

    player1.apply_gravity()
    player1.check_ground()
    
    player1.render(window)



    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player1.move_left()
    if keys[pygame.K_d]:
        if player1.move_right():
            break
    if keys[pygame.K_s]:
        player1.ground_pound()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_width = config.window_width = config.window_width / 2
                window_height = config.window_height = config.window_height / 2
                ground_height = config.ground_height = int(config.window_height * 0.2)
                window = pygame.display.set_mode((config.window_width, config.window_height))
                backdrop.change_background_size(config.window_width, config.window_height)
                player1.change_size(window_width, window_height)

            if event.key == pygame.K_w:
                player1.jump()

    if frame_count % 1 == 0:
        pygame.image.save(window, f'screenshots/screenshot{frame_count // 10}.png')

    frame_count += 1
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()