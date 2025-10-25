import pygame
from config import *
import math

class Tower:
    def __init__(self, x, y, tower_info):
        self.x = x
        self.y = y
        self.damage = tower_info["damage"]
        self.range = tower_info["range"]
        self.cooldown_max = tower_info["cooldown"]
        self.cooldown = 0
        self.color = tower_info["color"]
        self.level = 1
        self.upgrade_cost = tower_info["cost"]
        self.kill_xp = 0

    def can_attack(self, enemy):
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        return math.sqrt(dx*dx + dy*dy) <= self.range

    def attack(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for enemy in enemies:
            if self.can_attack(enemy):
                enemy.health -= self.damage
                self.cooldown = self.cooldown_max
                break

    # 🟦 Upgrades
    def upgrade_damage(self):
        self.damage += DAMAGE_UP_AMOUNT
        self.upgrade_cost = int(self.upgrade_cost * UPGRADE_COST_MULTIPLIER)

    def upgrade_range(self):
        self.range += RANGE_UP_AMOUNT
        self.upgrade_cost = int(self.upgrade_cost * UPGRADE_COST_MULTIPLIER)

    def upgrade_cooldown(self):
        self.cooldown_max = max(MIN_COOLDOWN, self.cooldown_max + COOLDOWN_UP_AMOUNT)
        self.upgrade_cost = int(self.upgrade_cost * UPGRADE_COST_MULTIPLIER)

    # 🟩 Selling
    def sell_value(self):
        return int(self.upgrade_cost * 0.5)

    # 🟨 XP System
    def add_xp(self):
        self.kill_xp += XP_PER_KILL
        if self.kill_xp >= XP_TO_NEXT_LEVEL:
            self.level += 1
            self.kill_xp = 0
            self.damage += 2  # bonus auto-upgrade
            self.range += 10
            print(f"Tower leveled up! Level: {self.level}")

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), 12)
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.range, 1)
