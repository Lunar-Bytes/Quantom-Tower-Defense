import pygame
from config import *

class Enemy:
    def __init__(self, path):
        self.path = path
        self.x, self.y = self.path[0]
        self.path_index = 0
        self.speed = ENEMY_SPEED
        self.health = 30
        self.max_health = self.health

    def move(self):
        if self.path_index + 1 < len(self.path):
            target_x, target_y = self.path[self.path_index + 1]
            dir_x = target_x - self.x
            dir_y = target_y - self.y
            dist = (dir_x**2 + dir_y**2)**0.5
            if dist != 0:
                dir_x /= dist
                dir_y /= dist
            self.x += dir_x * self.speed
            self.y += dir_y * self.speed
            if abs(target_x - self.x) < 5 and abs(target_y - self.y) < 5:
                self.path_index += 1

    def draw(self, win):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), 10)
        # Health bar
        pygame.draw.rect(win, RED, (self.x - 10, self.y - 15, 20, 4))
        pygame.draw.rect(win, GREEN, (self.x - 10, self.y - 15, 20 * (self.health / self.max_health), 4))
