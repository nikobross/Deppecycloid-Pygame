import pygame
import sys
import math
import random
from wheel import Wheel
from backdrop import Backdrop
from powerups import Powerups
import time
import config



window_width = config.window_width
window_height = config.window_height
ground_height = config.ground_height

max_health = 500

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

    # global health1
    # global health2
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
        player2.got_hit()

    if distance2 < rad2 * 2:
        reset_players()
        add_powerup = True
        player1.got_hit()

def check_player_spike_collisions_remake(player1, player2):

    global add_powerup

    player_pairs = [(player1, player2), (player2, player1)]

    rad = player1.radius    

    for player1, player2 in player_pairs:

        x2 = player2.circle_x
        y2 = player2.circle_y

        for spike_pair in player1.spikes_on_screen:
            spike_x = spike_pair[0]
            spike_y = spike_pair[1]

            dx = spike_x - x2
            dy = spike_y - y2

            distance = math.sqrt(dx * dx + dy * dy)

            if distance < rad * 2:
                reset_players()
                add_powerup = True
                player2.got_hit()

def render_scores():

    pygame.draw.rect(window, (0, 0, 0), (30, 10, max_health, 40))  # Health bar for player1
    pygame.draw.rect(window, (0, 0, 0), (window_width - max_health - 30, 10, max_health, 40))

    pygame.draw.rect(window, (255, 255, 0), (40, 20, player1.health - 20, 20))  # Health bar for player1
    pygame.draw.rect(window, (255, 255, 0), (window_width - player2.health - 20, 20, player2.health - 20, 20))

def reset_players():
    player1.set(player1.radius, window_height // 2)
    player2.set(window_width - player2.radius, window_height // 2)

def game_over_check():

    if player1.health <= 0 or player2.health <= 0:
        restart_game = False
        powerups_to_draw.clear()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        player1.reset_health()
                        player2.reset_health()
                        restart_game = True
                        break
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                square_size = min(window_width, window_height) // 2
                square_x = (window_width - square_size) // 2.67
                square_y = (window_height - square_size) // 2

                end_screen_background = pygame.Surface((square_size * 1.5, square_size))
                end_screen_background.fill((173, 216, 230))

                window.blit(end_screen_background, (square_x, square_y))

                if player1.health <= 0 and player2.health <= 0:
                    end_screen_message = "It's a tie! Press R to restart or Q to quit."
                elif player1.health <= 0:
                    end_screen_message = "Player 2 wins! Press R to restart or Q to quit."
                elif player2.health <= 0:
                    end_screen_message = "Player 1 wins! Press R to restart or Q to quit."
                    
                end_screen_text = font_small.render(end_screen_message, True, (255, 255, 255))
                
                text_position = ((window_width - end_screen_text.get_width()) // 2, (window_height - end_screen_text.get_height()) // 2)

                player1.clear_powerups()
                player2.clear_powerups()

                window.blit(end_screen_text, text_position)

            if restart_game:
                break

            pygame.display.flip()

def clear_powerups(player1, player2):
    player1.clear_powerups()
    player2.clear_powerups()


pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
caption = pygame.display.set_caption("Deppecyloid")
pygame.mouse.set_visible(False)
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

    check_player_spike_collisions_remake(player1, player2)

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


    if (player1.health + player2.health) % 3 == 0 and (player1.health + player2.health) != 500:
        if not powerup_on_screen and add_powerup:
            clear_powerups(player1, player2)
            powerup1 = Powerups()
            powerups_to_draw.append(powerup1)
            powerup_on_screen = True
            add_powerup = False




    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player2.move_left()
    if keys[pygame.K_RIGHT]:
        player2.move_right()
    if keys[pygame.K_DOWN]:
        player2.ground_pound()

    if keys[pygame.K_a]:
        player1.move_left()
    if keys[pygame.K_d]:
        player1.move_right()
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
                player2.change_size(window_width, window_height)
        
            if event.key == pygame.K_UP:
                player2.jump()
            if event.key == pygame.K_w:
                player1.jump()

    pygame.display.flip()
    clock.tick(60)