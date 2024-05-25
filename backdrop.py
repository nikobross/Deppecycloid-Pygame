import pygame
import sys
import math
import random
import config

window_width = config.window_width
window_height = config.window_height

class Backdrop():
    def __init__ (self, background):

        if background == "blue_sky":
            self.backdrop = pygame.image.load('background1.jpeg')
            self.backdrop = pygame.transform.scale(self.backdrop, (window_width, window_height))
        else:
            self.backdrop = pygame.image.load('background1.jpeg')
            self.backdrop = pygame.transform.scale(self.backdrop, (window_width, window_height))

        self.ground_height = int(window_height * 0.1)


    def change_background(self, background):
        if background == "blue_sky":
            self.backdrop = pygame.image.load('background1.jpeg')
            self.backdrop = pygame.transform.scale(self.backdrop, (window_width, window_height))
        else:
            self.backdrop = pygame.image.load('background1.jpeg')
            self.backdrop = pygame.transform.scale(self.backdrop, (window_width, window_height))
    
    def change_background_size(self, width, height):
        self.backdrop = pygame.transform.scale(self.backdrop, (width, height))