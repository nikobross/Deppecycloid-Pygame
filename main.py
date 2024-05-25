import pygame
import sys
import math
import random
from wheel import Wheel
from backdrop import Backdrop
from powerups import Powerups
import time


window_width = 1400
window_height = 800

score1 = 0
score2 = 0

powerups_to_draw = []
powerup_on_screen = False
add_powerup = True

def check_player_collisions(player1, player2):

    rad1 = player1.radius
    rad2 = player2.radius

    x1 = player1.circle_x
    x2 = player2.circle_x

    y1 = player1.circle_y
    y2 = player2.circle_y

    dx = x1 - x2
    dy = y1 - y2
    distance = math.sqrt(dx * dx + dy * dy)

    dx = (x1 + rad1) - (x2+ rad2)
    dy = (y1 + rad1) - (y2 + rad2)
    distance = math.sqrt(dx * dx + dy * dy)

    if distance < rad1 * 2 + rad2 * 2:
        overlap = (rad1 * 2 + rad2 * 2) - distance

        if distance != 0:
            dx /= distance
            dy /= distance

        player1.change_x(overlap * dx / 2)
        player1.change_y(overlap * dy / 2)
        player2.change_x(-overlap * dx / 2)
        player2.change_y(-overlap * dy / 2)

def check_player_spike_collisions(player1, player2):

    global score1
    global score2
    global add_powerup

    rad1 = player1.radius
    rad2 = player2.radius

    x1 = player1.circle_x
    x2 = player2.circle_x

    y1 = player1.circle_y
    y2 = player2.circle_y

    spike1_x = player1.spike_x
    spike1_y = player1.spike_y

    spike2_x = player2.spike_x
    spike2_y = player2.spike_y

    dx1 = spike1_x - x2
    dy1 = spike1_y - y2
    distance1 = math.sqrt(dx1 * dx1 + dy1 * dy1)

    dx2 = spike2_x - x1
    dy2 = spike2_y - y1
    distance2 = math.sqrt(dx2 * dx2 + dy2 * dy2)

    if distance1 < rad1 * 2:
        reset_players()
        add_powerup = True
        score1 += 1

    if distance2 < rad2 * 2:
        reset_players()
        add_powerup = True
        score2 += 1

def render_scores():
    score1_text = font_big.render(str(score1), True, (255, 255, 255))
    score2_text = font_big.render(str(score2), True, (255, 255, 255))

    window.blit(score1_text, (10, 10))
    window.blit(score2_text, (window_width - score2_text.get_width() - 10, 10))

def reset_players():
    player1.set(player1.radius, window_height // 2)
    player2.set(window_width - player2.radius, window_height // 2)

def game_over_check():

    global score1
    global score2

    if score1 >= 10 or score2 >= 10:
        restart_game = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press R to restart
                        score1 = 0
                        score2 = 0
                        restart_game = True
                        break  # Break the inner loop
                    elif event.key == pygame.K_q:  # Press Q to quit
                        pygame.quit()
                        sys.exit()
                        
                end_screen_background = pygame.Surface((window_width, window_height))
                end_screen_background.fill((173, 216, 230))  # RGB color for blue

                # Draw the end screen background onto the screen
                window.blit(end_screen_background, (0, 0))
                
                end_screen_message = "Game Over. Press R to restart or Q to quit."
                if score1 >= 10:
                    end_screen_message = "Player 1 wins! Press R to restart or Q to quit. " + str(score1) + "-" + str(score2)
                if score2 >= 10:
                    end_screen_message = "Player 2 wins! Press R to restart or Q to quit. " + str(score1) + "-" + str(score2)
                    
                end_screen_text = font_small.render(end_screen_message, True, (255, 255, 255))
                
                text_position = ((window_width - end_screen_text.get_width()) // 2, (window_height - end_screen_text.get_height()) // 2)

                # Draw the text onto the screen
                window.blit(end_screen_text, text_position)

            if restart_game:
                break

            pygame.display.flip()

def clear_powerups(player1, player2):
    player1.clear_powerups()
    player2.clear_powerups()


pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((window_width, window_height))
caption = pygame.display.set_caption("Deppecyloid")
font_small = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 100)


backdrop = Backdrop("blue_sky")

player1 = Wheel("Bike")
player1.set(player1.radius, window_height // 2)

player2 = Wheel("BeachBall")
player2.set(window_width - player2.radius, window_height // 2)

while True:

    
    window.blit(backdrop.backdrop, (0, 0))

    player1.apply_gravity()
    player1.check_ground()

    player2.apply_gravity()
    player2.check_ground()

    check_player_collisions(player1, player2)

    check_player_spike_collisions(player1, player2)

    for powerup in powerups_to_draw:
        powerup.render(window)
        if powerup.check_collision(player1):
            player1.get_powerup(powerup)
            powerups_to_draw.remove(powerup)
            powerup_on_screen = False
        if powerup.check_collision(player2):
            player2.get_powerup(powerup)
            powerups_to_draw.remove(powerup)
            powerup_on_screen = False

    render_scores()
    game_over_check()
    
    player1.render(window)
    player2.render(window)


    if (score1 + score2) % 3 == 0 and (score1 + score2) != 0:
        if not powerup_on_screen and add_powerup:
            clear_powerups(player1, player2)
            powerup1 = Powerups()
            powerups_to_draw.append(powerup1)
            powerup_on_screen = True
            add_powerup = False




    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player1.move_left()
    if keys[pygame.K_RIGHT]:
        player1.move_right()
    if keys[pygame.K_DOWN]:
        player1.ground_pound()

    if keys[pygame.K_a]:
        player2.move_left()
    if keys[pygame.K_d]:
        player2.move_right()
    if keys[pygame.K_s]:
        player2.ground_pound()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.jump()
            if event.key == pygame.K_w:
                player2.jump()

    pygame.display.flip()
    clock.tick(60)