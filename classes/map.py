import pygame
from config import *

class GameMap:
    def __init__(self):
        # Example path
        self.path = [(50, 50), (750, 50), (750, 550), (50, 550)]

    def draw(self, WIN):
        # Draw path
        for i in range(len(self.path)-1):
            pygame.draw.line(WIN, WHITE, self.path[i], self.path[i+1], 5)
