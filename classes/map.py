import pygame
from config import *

class GameMap:
    def __init__(self):
        # Simple path as a list of points
        self.path = [(50, 50), (750, 50), (750, 550), (50, 550)]

    def draw(self, win):
        # Draw path
        if len(self.path) > 1:
            pygame.draw.lines(win, GREEN, False, self.path, 5)
