import pygame
from config import *
from classes.projectile import Projectile
from utils.helpers import distance

class Tower:
    def __init__(self, x, y, tower_type="normal"):
        self.x = x
        self.y = y
        self.type = tower_type
        stats = TOWER_TYPES[self.type]
        self.range = stats["range"]
        self.damage = stats["damage"]
        self.cooldown = stats["cooldown"]
        self.timer = 0

    def update(self, enemies, projectiles):
        if self.timer > 0:
            self.timer -= 1
        else:
            for enemy in enemies:
                if distance((self.x, self.y), (enemy.x, enemy.y)) <= self.range:
                    projectiles.append(Projectile(self.x, self.y, enemy, self.damage))
                    self.timer = self.cooldown
                    break

    def draw(self, win, selected_tower):
        # Tower color
        color = BLUE if self.type == "normal" else PURPLE
        pygame.draw.circle(win, color, (self.x, self.y), 15)
        # Show range only if selected
        if self == selected_tower:
            pygame.draw.circle(win, color, (self.x, self.y), self.range, 1)
