import pygame
import sys
import math
import random
import config



class Wheel(pygame.sprite.Sprite):
    def __init__(self, skin):
        super().__init__()
        if skin == "Bike":
            self.original_image = pygame.image.load('BikeWheelSpike.png')
        if skin == "BeachBall":
            self.original_image = pygame.image.load('BeachBallSpike.png')
        
        self.radius = int(min(config.window_width, config.window_height) * 0.05)
        self.original_image = pygame.transform.scale(self.original_image, (int(self.radius*5.6), int(self.radius*5.6)))
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
        self.x_velocity = int(config.window_width * 0.012)
        self.rotation_velocity = 6

        self.circle_x = self.radius

        self.circle_dy = 0
        self.circle_y = 0
        
        self.angle = 0
        self.gravity = 1

        self.jump_speed = 23
        self.jumping = False

        self.jumps_remaining = 1
        self.max_jumps = 1

        self.active_powerups = []

        self.angle_rad = math.radians(self.angle) + math.pi / 2

        self.ground_pounding = False

        self.spike_x = self.circle_x + self.radius * math.cos(self.angle_rad) * 2.6
        self.spike_y = self.circle_y - self.radius * math.sin(self.angle_rad) * 2.6
        self.spike_width = 5

    def rotate(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)

    def render(self, window):

        for powerup in self.active_powerups:
            if powerup == 'speed':
                self.x_velocity = 1.5 * int(config.window_width * 0.012)
                self.rotation_velocity = 9
            if powerup == 'jump':
                self.max_jumps = 2

        self.move_spike()
        self.rect = self.image.get_rect(center = (self.circle_x, self.circle_y))
        window.blit(self.image, self.rect.topleft)

        #pygame.draw.line(window, (0, 0, 0), (self.circle_x, self.circle_y), (self.spike_x, self.spike_y), self.spike_width)

    def apply_gravity(self):
        self.circle_dy += self.gravity
        self.circle_y += self.circle_dy

    def check_ground(self):
        if self.circle_y + self.radius*2 > config.window_height - config.ground_height:
            self.circle_y = config.window_height - self.radius*2 - config.ground_height
            self.circle_dy = 0
            self.jumping = False
            self.ground_pounding = False
            self.jumps_remaining = self.max_jumps

    def move_left(self):
        self.circle_x -= self.x_velocity
        self.rotate(self.rotation_velocity)
        if self.circle_x + self.radius*2 < 0:
            self.circle_x = config.window_width - self.radius*2
    
    def move_right(self):
        self.circle_x += self.x_velocity
        self.rotate(-self.rotation_velocity)
        if self.circle_x - self.radius*2 > config.window_width:
            self.circle_x = 0

    def set(self, x , y):
        self.circle_x = x
        self.circle_y = y
        # self.angle = 0
        # self.image = pygame.transform.rotate(self.original_image, self.angle)
        # self.rect = self.image.get_rect(center=self.rect.center)

    def move_spike(self):

        self.angle_rad = math.radians(self.angle) + math.pi / 2

        self.spike_x = self.circle_x + self.radius * math.cos(self.angle_rad) * 2.6
        self.spike_y = self.circle_y - self.radius * math.sin(self.angle_rad) * 2.6

    def jump(self):
        if self.jumps_remaining > 0:
                self.circle_dy -= self.jump_speed
                self.jumping = True
                self.jumps_remaining -= 1

    def get_rect(self):
        self.rect = self.image.get_rect(center = (self.circle_x, self.circle_y))
        return self.rect

    def change_x(self, dx):
        self.circle_x += dx

    def change_y(self, dy):
        self.circle_y += dy

    def get_powerup(self, powerup):
        powerup_name = powerup.type
        self.active_powerups.append(powerup_name)

        if powerup_name == 'jump':
            self.jumps_remaining = 1
            
    def ground_pound(self):
        if not self.ground_pounding:
            self.circle_dy = 50
            self.ground_pounding = True

    def clear_powerups(self):
        self.active_powerups = []
        self.jumps_remaining = 1
        self.max_jumps = 1
        self.x_velocity = int(config.window_width * 0.012)
        self.rotation_velocity = 6

    def change_size(self, width, height):
        self.radius = int(min(width, height) * 0.05)
        self.original_image = pygame.transform.scale(self.original_image, (int(self.radius*5.6), int(self.radius*5.6)))


