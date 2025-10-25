import pygame

class Projectile:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 5

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = (dx**2 + dy**2)**0.5
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

    def hit_target(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        if (dx**2 + dy**2)**0.5 < 5:
            self.target.health -= self.damage
            return True
        return False

    def draw(self, WIN):
        pygame.draw.circle(WIN, (255, 255, 0), (int(self.x), int(self.y)), 5)
