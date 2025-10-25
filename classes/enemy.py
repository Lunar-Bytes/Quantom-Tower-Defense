import pygame
from config import *

class Enemy:
    def __init__(self, path, enemy_type="basic"):
        self.path = path
        self.path_index = 0
        self.enemy_type = enemy_type  # Use this consistently
        self.speed = ENEMY_SPEED
        self.health = 10
        self.max_health = 10
        self.radius = 10
        self.color = ENEMY_COLORS.get(self.enemy_type, WHITE)
        self.x, self.y = path[0]

        # Adjust stats based on type
        if self.enemy_type == "fast":
            self.speed *= 1.5
            self.health = self.max_health = 20
        elif self.enemy_type == "tank":
            self.speed *= 0.7
            self.health = self.max_health = 50
        # Default "basic" already set above

    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                dx, dy = dx / dist, dy / dist
                self.x += dx * self.speed
                self.y += dy * self.speed
            if abs(self.x - target_x) < self.speed and abs(self.y - target_y) < self.speed:
                self.path_index += 1

    def draw(self, win):
        # Draw enemy circle
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

        # Draw health bar above enemy
        health_bar_width = self.radius * 2
        health_ratio = self.health / self.max_health
        pygame.draw.rect(win, RED, (int(self.x - self.radius), int(self.y - self.radius - 10), health_bar_width, 5))
        pygame.draw.rect(win, (0, 255, 0),
                         (int(self.x - self.radius), int(self.y - self.radius - 10), int(health_bar_width * health_ratio), 5))
