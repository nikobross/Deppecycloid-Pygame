from itertools import groupby
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
            self.double_spike_image_original = pygame.image.load('BikeWheelDoubleSpike.png')
        if skin == "BeachBall":
            self.original_image = pygame.image.load('BeachBallSpike.png')
            self.double_spike_image_original = pygame.image.load('BeachBallDoubleSpike.png')
        
        self.radius = int(min(config.window_width, config.window_height) * 0.05)
        self.original_image = pygame.transform.scale(self.original_image, (int(self.radius*5.6), int(self.radius*5.6)))
        self.double_spike_image_original = pygame.transform.scale(self.double_spike_image_original, (int(self.radius*5.6), int(self.radius*5.6)))
        self.original_original_image = self.original_image.copy()
        
        self.double_spike_image = self.double_spike_image_original.copy()
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.health = 500
        
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

        self.double_spike = False

        self.angle_rad = math.radians(self.angle) + math.pi / 2
        self.angle_rad2 = math.radians(self.angle) - math.pi / 2

        self.ground_pounding = False

        self.spike_x = self.circle_x + self.radius * math.cos(self.angle_rad) * 2.6
        self.spike_y = self.circle_y - self.radius * math.sin(self.angle_rad) * 2.6

        self.spike_x2 = self.circle_x + self.radius * math.cos(self.angle_rad2) * 2.6
        self.spike_y2 = self.circle_y - self.radius * math.sin(self.angle_rad2) * 2.6

        self.spikes_on_screen = [(self.spike_x, self.spike_y)]

        self.spike_width = 5

        self.spike_path = []

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
            if powerup == 'spike':
                self.double_spike = True

        self.move_spikes()
        self.rect = self.image.get_rect(center = (self.circle_x, self.circle_y))
        window.blit(self.image, self.rect.topleft)

        # path_segments = [list(g) for k, g in groupby(self.spike_path, lambda x: x is None) if not k]
        # for segment in path_segments:
        #     if len(segment) > 1:
        #         pygame.draw.lines(window, (0, 0, 0), False, segment, self.spike_width)

        # pygame.draw.line(window, (0, 0, 0), (self.circle_x, self.circle_y), (self.spike_x, self.spike_y), self.spike_width)
        # pygame.draw.line(window, (0, 0, 0), (self.circle_x, self.circle_y), (self.spike_x2, self.spike_y2), self.spike_width)

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
            return True
        return False

    def set(self, x , y):
        self.circle_x = x
        self.circle_y = y

        self.spike_x = self.circle_x + self.radius * math.cos(0) * 2.6
        self.spike_y = self.circle_y - self.radius * math.sin(0) * 2.6

        self.spike_x2 = self.circle_x + self.radius * math.cos(0) * 2.6
        self.spike_y2 = self.circle_y - self.radius * math.sin(0) * 2.6
        # self.angle = 0
        # self.image = pygame.transform.rotate(self.original_image, self.angle)
        # self.rect = self.image.get_rect(center=self.rect.center)

    def move_spikes(self):
        self.angle_rad = math.radians(self.angle) + math.pi / 2

        new_spike_x = self.circle_x + self.radius * math.cos(self.angle_rad) * 2.6
        new_spike_y = self.circle_y - self.radius * math.sin(self.angle_rad) * 2.6

        # Check if the wheel has crossed the screen boundary
        # if self.spike_path and abs(new_spike_x - self.spike_path[-1][0]) > self.radius:
        #     # If it has, start a new line segment for the path
        #     self.spike_path.append(None)

        self.spike_x = new_spike_x
        self.spike_y = new_spike_y

        self.spike_path.append((self.spike_x, self.spike_y))

        if self.double_spike:
            self.angle_rad2 = math.radians(self.angle) - math.pi / 2

            self.spike_x2 = self.circle_x + self.radius * math.cos(self.angle_rad2) * 2.6
            self.spike_y2 = self.circle_y - self.radius * math.sin(self.angle_rad2) * 2.6

            self.spikes_on_screen = [(self.spike_x, self.spike_y), (self.spike_x2, self.spike_y2)]

        else:
            self.spikes_on_screen = [(self.spike_x, self.spike_y)]

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
        if powerup_name == 'spike':
            self.image = self.double_spike_image.copy()
            self.original_image = self.double_spike_image_original.copy()
            
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
        self.double_spike = False
        self.original_image = self.original_original_image.copy()
        self.image = self.original_image.copy()

    def change_size(self, width, height):
        self.radius = int(min(width, height) * 0.05)
        self.original_image = pygame.transform.scale(self.original_image, (int(self.radius*5.6), int(self.radius*5.6)))

    def move_spike2(self):
        self.angle_rad2 = math.radians(self.angle) - math.pi / 2

        self.spike_x2 = self.circle_x + self.radius * math.cos(self.angle_rad2) * 2.6
        self.spike_y2 = self.circle_y - self.radius * math.sin(self.angle_rad2) * 2.6

    def got_hit(self):
        self.health -= 50

    def reset_health(self):
        self.health = 500



