import pygame
from config import *

class Enemy:
    def __init__(self, path, enemy_type="basic"):
        self.path = path
        self.path_index = 0
        self.x, self.y = path[0]
        self.type = enemy_type
        self.speed = ENEMY_SPEEDS.get(enemy_type, 1.0)
        self.color = ENEMY_COLORS.get(enemy_type, WHITE)

        if enemy_type == "basic":
            self.health = self.max_health = 10
        elif enemy_type == "fast":
            self.health = self.max_health = 20
        elif enemy_type == "tank":
            self.health = self.max_health = 50
        else:
            self.health = self.max_health = 10

        self.radius = 15

    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = (dx**2 + dy**2)**0.5
            if dist <= self.speed:
                # Reached next point
                self.x, self.y = target_x, target_y
                self.path_index += 1
            else:
                # Move toward next point
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed

    def draw(self, WIN):
        pygame.draw.circle(WIN, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw health bar
        health_ratio = self.health / self.max_health
        bar_width = self.radius*2
        bar_height = 5
        pygame.draw.rect(WIN, RED, (self.x - self.radius, self.y - self.radius - 10, bar_width, bar_height))
        pygame.draw.rect(WIN, GREEN, (self.x - self.radius, self.y - self.radius - 10, bar_width * health_ratio, bar_height))
