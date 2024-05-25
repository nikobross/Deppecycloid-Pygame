import pygame
import sys
import math
import random


powerups = ["Speed", "Quad Spike", "Double Jump", "Shield"]
powerups_on_screen = []
powerup_active = False
powerup_x = 0
powerup_y = 0

speed = pygame.image.load('Speed.png')
speed = pygame.transform.scale(speed, (100, 100))

spike = pygame.image.load('Spike.png')
spike = pygame.transform.scale(spike, (100, 100))

jump = pygame.image.load('DoubleJump.png')
jump = pygame.transform.scale(jump, (100, 100))

shield = pygame.image.load('Shield.png')
shield = pygame.transform.scale(shield, (100, 100))

def randomize_powerups():
    # Randomize the powerups
    powerup1 = random.choice(powerups)
    
    powerups_on_screen.append(powerup1)

    return powerup1

def random_placement():
    # Randomize the placement of the powerups
    powerup_x = random.randint(0, window_width - 100)
    powerup_y = random.randint(0, window_height - 100)

    return powerup_x, powerup_y

def draw_powerups(powerup_x, powerup_y):
    # Draw the powerups
    
    for powerup in powerups_on_screen:
        if powerup == "Speed":
            window.blit(speed, (powerup_x, powerup_y))
            #pygame.draw.rect(window, (255, 0, 0), pygame.Rect(powerup_x, powerup_y, 50, 50))
        elif powerup == "Quad Spike":
            window.blit(spike, (powerup_x, powerup_y))
            #pygame.draw.rect(window, (0, 0, 255), pygame.Rect(powerup_x, powerup_y, 50, 50))
        elif powerup == "Double Jump":
            window.blit(jump, (powerup_x, powerup_y))
            #pygame.draw.rect(window, (0, 255, 0), pygame.Rect(powerup_x, powerup_y, 50, 50))
        elif powerup == "Shield":
            window.blit(shield, (powerup_x, powerup_y))
            #pygame.draw.rect(window, (255, 255, 0), pygame.Rect(powerup_x, powerup_y, 50, 50))

    return powerup_x, powerup_y


# Initialize Pygame
pygame.init()

# Set up the window
window_width = 1400
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
# window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
pygame.display.set_caption("Deppecyloid")
font_small = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 100)

backdrop = pygame.image.load('background1.jpeg')
backdrop = pygame.transform.scale(backdrop, (1400, 900))

# Set up the clock
clock = pygame.time.Clock()

# Game loop
ground_height = int(window_height * 0.1)  # 10% of the window height
ground_color = (0, 255, 0)

# Set up the background
background_color = (173, 216, 230)

# Set up the circle
circle_radius = int(min(window_width, window_height) * 0.05)  # 5% of the smallest window dimension
circle_x = circle_radius  # Start at the left side of the screen
circle_y = window_height // 2  # Start in the middle of the screen
circle_dy = 0  # Vertical speed of the circle

# Load the sprite
initial_x1 = circle_x
initial_y1 = circle_y
sprite = pygame.image.load('BikeWheelSpike.png')
sprite = pygame.transform.scale(sprite, (int(circle_radius*5.6), int(circle_radius*5.6)))  # Scale the sprite to double the desired size


jumping1 = False
jumping2 = False
jump_speed = 23
gravity = 1

# Set up the rotation
angle = 0

score1 = 0
score2 = 0

# Load the second sprite
sprite2 = pygame.image.load('BeachBallSpike.png')
sprite2 = pygame.transform.scale(sprite2, (int(circle_radius*5.6), int(circle_radius*5.6)))

# Set up the second circle
circle2_x = window_width - circle_radius*2  # Start at the right side of the screen
circle2_y = window_height // 2  # Start in the middle of the screen
circle2_dy = 0  # Vertical speed of the second circle

initial_x2 = circle2_x
initial_y2 = circle2_y

# Set up the rotation for the second sprite
angle2 = 0

spike_width = 5  # The width of the spike


# Game loop
while True:
    # Handle events
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key presses
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        circle_x -= int(window_width * 0.012)  # 1% of the window width
        angle += 6  # Rotate counter-clockwise
        if circle_x + circle_radius*2 < 0:  # If the sprite has gone off the left side of the screen
            circle_x = window_width - circle_radius*2  # Move it to the right side of the screen
    if keys[pygame.K_d]:
        circle_x += int(window_width * 0.012)  # 1% of the window width
        angle -= 6  # Rotate clockwise
        if circle_x - circle_radius*2 > window_width:  # If the sprite has gone off the right side of the screen
            circle_x = 0  # Move it to the left side of the screen


    if keys[pygame.K_LEFT]:
        circle2_x -= int(window_width * 0.012)  # Increase by 20%
        angle2 += 6  # Increase by 20%
        if circle2_x + circle_radius*2 < 0:  # If the sprite has gone off the left side of the screen
            circle2_x = window_width - circle_radius*2  # Move it to the right side of the screen
    if keys[pygame.K_RIGHT]:
        circle2_x += int(window_width * 0.012)  # Increase by 20%
        angle2 -= 6  # Increase by 20%
        if circle2_x - circle_radius*2 > window_width:  # If the sprite has gone off the right side of the screen
            circle2_x = 0  # Move it to the left side of the screen
    
    if keys[pygame.K_UP] and not jumping2:
        jumping2 = True
        circle2_dy = -jump_speed
    
    if keys[pygame.K_w] and not jumping1:
        jumping1 = True
        circle_dy = -jump_speed
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit fullscreen mode when the ESC key is pressed
                screen = pygame.display.set_mode((800, 600))  # Change to your desired window size

    
    # Apply acceleration
    circle_dy += gravity
    circle_y += circle_dy
    circle2_dy += gravity
    circle2_y += circle2_dy

 # Calculate the angle of rotation in radians
    angle_rad = math.radians(angle) + math.pi / 2
    angle2_rad = math.radians(angle2) + math.pi / 2

    # Calculate the new position of the spikes
    spike1_x = circle_x + circle_radius * math.cos(angle_rad) * 2.6
    spike1_y = circle_y - circle_radius * math.sin(angle_rad) * 2.6
    spike2_x = circle2_x + circle_radius * math.cos(angle2_rad) * 2.6
    spike2_y = circle2_y - circle_radius * math.sin(angle2_rad) * 2.6
    
    if circle_y + circle_radius*2 > window_height - ground_height:  # Adjusted for the new sprite size
        circle_y = window_height - ground_height - circle_radius*2  # Adjusted for the new sprite size
        circle_dy = 0  # Stop falling when hitting the ground
        jumping1 = False
        
    if circle2_y + circle_radius*2 > window_height - ground_height:  # Adjusted for the new sprite size
        circle2_y = window_height - ground_height - circle_radius*2  # Adjusted for the new sprite size
        circle2_dy = 0  # Stop falling when hitting the ground
        jumping2 = False
        
    wheel1_rect = pygame.Rect(circle_x - circle_radius, circle_y - circle_radius, circle_radius * 2, circle_radius * 2)
    wheel2_rect = pygame.Rect(circle2_x - circle_radius, circle2_y - circle_radius, circle_radius * 2, circle_radius * 2)
    
        # Calculate the distance between the centers of the two circles
    dx = circle_x - circle2_x
    dy = circle_y - circle2_y
    distance = math.sqrt(dx * dx + dy * dy)

    # Check for collisions
    dx = (circle_x + circle_radius) - (circle2_x + circle_radius)
    dy = (circle_y + circle_radius) - (circle2_y + circle_radius)
    distance = math.sqrt(dx * dx + dy * dy)

    # Check for collisions
    if distance < circle_radius * 2 + circle_radius * 2:  # The diameters of the two circles
        # Calculate the overlap
        overlap = (circle_radius * 2 + circle_radius * 2) - distance

        # Normalize the direction vector
        if distance != 0:
            dx /= distance
            dy /= distance

        # Move the circles away from each other
        circle_x += overlap * dx / 2
        circle_y += overlap * dy / 2
        circle2_x -= overlap * dx / 2
        circle2_y -= overlap * dy / 2
    
    dx1 = spike1_x - circle2_x
    dy1 = spike1_y - circle2_y
    distance1 = math.sqrt(dx1 * dx1 + dy1 * dy1)

    dx2 = spike2_x - circle_x
    dy2 = spike2_y - circle_y
    distance2 = math.sqrt(dx2 * dx2 + dy2 * dy2)

    # Check if the spikes hit the other circle
    if distance1 < circle_radius * 2:  # Add the length of the spike to the radius
        score1 += 1

        # Teleport the circles back to their starting positions
        circle_x = initial_x1
        circle_y = initial_y1
        circle2_x = initial_x2
        circle2_y = initial_y2

    if distance2 < circle_radius * 2:  # Add the length of the spike to the radius
        score2 += 1

        # Teleport the circles back to their starting positions
        circle_x = initial_x1
        circle_y = initial_y1
        circle2_x = initial_x2
        circle2_y = initial_y2

    
    for powerup in powerups_on_screen:
        if pygame.sprite.spritecollide(powerup, sprite, False):
            if powerup == "Speed":
                jump_speed = 30
                powerups_on_screen.remove(powerup)
            elif powerup == "Quad Spike":
                spike_width = 10
                powerups_on_screen.remove(powerup)
            elif powerup == "Double Jump":
                gravity = 0.5
                powerups_on_screen.remove(powerup)
            elif powerup == "Shield":
                circle_radius = 50
                powerups_on_screen.remove(powerup)



    # Rotate the sprites
    rotated_sprite = pygame.transform.rotate(sprite, angle)
    rotated_sprite2 = pygame.transform.rotate(sprite2, angle2)
    
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
                        powerups_on_screen.clear()
                        print("Restarting the game...")
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
                break  # Break the outer loop

        # Rest of your game code...



            # Render the end screen message

            
            pygame.display.flip()
    

    
    
    # Clear the window with the background color
    window.fill(background_color)

    # Draw the ground
    pygame.draw.rect(window, ground_color, pygame.Rect(0, window_height - ground_height, window_width, ground_height))
    
    window.blit(backdrop, (0, 0))

    # Draw the rotated sprites
    sprite_rect = rotated_sprite.get_rect(center = (circle_x, circle_y))  # Get the rectangle that contains the rotated sprite
    window.blit(rotated_sprite, sprite_rect.topleft)  # Draw the rotated sprite
    sprite2_rect = rotated_sprite2.get_rect(center = (circle2_x, circle2_y))  # Get the rectangle that contains the rotated sprite
    window.blit(rotated_sprite2, sprite2_rect.topleft)  # Draw the rotated sprite
    
    
    
    
    
    # Render the scores as text
    score1_text = font_big.render(str(score1), True, (255, 255, 255))
    score2_text = font_big.render(str(score2), True, (255, 255, 255))
    
    
    if score1 + score2 == 5 and not powerup_active:
        print('powerup')
        powerup1 = randomize_powerups()
        powerup_x, powerup_y = random_placement() 
        
        powerup_active = True

    draw_powerups(powerup_x, powerup_y)
    
    # if powerup1 == "speed":
    #         pygame.draw.rect(window, (255, 0, 0), pygame.Rect(powerup_x, powerup_y, 50, 50))
    #     elif powerup1 == "Quad Spike":
    #         pygame.draw.rect(window, (0, 0, 255), pygame.Rect(powerup_x, powerup_y, 50, 50))
    #     else:
    #         pygame.draw.rect(window, (0, 255, 0), pygame.Rect(powerup_x, powerup_y, 50, 50))

    # Display the scores in the top corners of the screen
    window.blit(score1_text, (10, 10))
    window.blit(score2_text, (window_width - score2_text.get_width() - 10, 10))
    

    

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)