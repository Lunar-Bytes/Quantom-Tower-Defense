import pygame
from config import *

class Enemy:
    def __init__(self, path, enemy_type="basic"):
        self.path = path
        self.path_index = 0
        self.type = enemy_type
        self.speed = ENEMY_SPEED
        self.health = 10
        self.max_health = 10
        self.radius = 10
        self.color = ENEMY_COLORS.get(enemy_type, WHITE)
        self.x, self.y = path[0]

        # Adjust stats based on type
        if enemy_type == "fast":
            self.speed *= 1.5
            self.health = self.max_health = 20
        elif enemy_type == "tank":
            self.speed *= 0.7
            self.health = self.max_health = 50

    def move(self):
        if self.path_index < len(self.path)-1:
            target_x, target_y = self.path[self.path_index+1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                dx, dy = dx / dist, dy / dist
                self.x += dx * self.speed
                self.y += dy * self.speed
            if abs(self.x - target_x) < self.speed and abs(self.y - target_y) < self.speed:
                self.path_index += 1

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)
        # Health bar
        pygame.draw.rect(win, RED, (self.x - self.radius, self.y - self.radius - 10, self.radius*2, 5))
        pygame.draw.rect(win, (0,255,0), 
                         (self.x - self.radius, self.y - self.radius - 10, int(self.radius*2 * (self.health/self.max_health)), 5))
