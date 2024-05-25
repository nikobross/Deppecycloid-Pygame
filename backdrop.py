import pygame
import sys
import math
import random

window_width = 1400
window_height = 800

class Backdrop():
    def __init__ (self, background):

        if background == "blue_sky":
            self.backdrop = pygame.image.load('background1.jpeg')
            self.backdrop = pygame.transform.scale(self.backdrop, (1400, 900))
        else:
            self.backdrop = pygame.image.load('background1.jpeg')
            self.backdrop = pygame.transform.scale(self.backdrop, (1400, 900))

        self.ground_height = int(window_height * 0.1)