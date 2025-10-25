import pygame
from config import *
from classes.projectile import Projectile

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.type = tower_type
        self.color = TOWER_TYPES[tower_type]["color"]
        self.range = TOWER_TYPES[tower_type]["range"]
        self.damage = TOWER_TYPES[tower_type]["damage"]
        self.cooldown = TOWER_TYPES[tower_type]["cooldown"]
        self.timer = 0

    def update(self, enemies, projectiles):
        if self.timer > 0:
            self.timer -= 1
            return

        target = None
        for enemy in enemies:
            dist = ((self.x - enemy.x)**2 + (self.y - enemy.y)**2)**0.5
            if dist <= self.range:
                target = enemy
                break

        if target:
            projectiles.append(Projectile(self.x, self.y, target, self.damage))
            self.timer = self.cooldown

    def draw(self, WIN, selected_tower=None):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), 15)
        if selected_tower == self:
            pygame.draw.circle(WIN, (255, 215, 0), (self.x, self.y), self.range, 2)
