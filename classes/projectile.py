import pygame
from config import *

class Projectile:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 7
        self.active = True

    def move(self):
        if self.target.health <= 0:
            self.active = False
            return
        dir_x = self.target.x - self.x
        dir_y = self.target.y - self.y
        dist = (dir_x**2 + dir_y**2)**0.5
        if dist == 0:
            return
        dir_x /= dist
        dir_y /= dist
        self.x += dir_x * self.speed
        self.y += dir_y * self.speed

    def hit_target(self):
        dist = ((self.target.x - self.x)**2 + (self.target.y - self.y)**2)**0.5
        if dist < 10:
            self.target.health -= self.damage
            return True
        return False

    def draw(self, win):
        pygame.draw.circle(win, WHITE, (int(self.x), int(self.y)), 5)
