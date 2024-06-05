import pygame

# Initialize Pygame
pygame.init()

# Get screen resolution
infoObject = pygame.display.Info()

window_width = infoObject.current_w
window_height = int(infoObject.current_h * 0.8)  # Set window height to 80% of screen height
ground_height = int(window_height * 0.2)


print("window_width:", window_width)
print("window_height:", window_height)
print("ground_height:", ground_height)