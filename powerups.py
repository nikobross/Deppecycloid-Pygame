import pygame
import sys
import math
import random

powerups = ['speed', 'jump', 'spike']


class Powerups:

    

    def __init__(self):

        self.type = random.choice(powerups)
        
        if self.type == 'speed':
            self.image = pygame.image.load('Speed.png')
        if self.type == 'jump':
            self.image = pygame.image.load('DoubleJump.png')
        # if self.type == 'shield':
        #     self.image = pygame.image.load('Shield.png')
        if self.type == 'spike':
            self.image = pygame.image.load('Spike.png')

        self.image = pygame.transform.scale(self.image, (120, 120))

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(300, 950)
        self.rect.y = random.randint(250, 600)

        self.rect.width = 50
        self.rect.height = 50
    
    def render(self, window):
        window.blit(self.image, self.rect.topleft)
    
    def check_collision(self, player):
        if self.rect.colliderect(player.get_rect()):
            return True
        return False