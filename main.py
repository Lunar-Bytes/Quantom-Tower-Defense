import pygame
import sys
import json
from config import *
from classes.enemy import Enemy
from classes.tower import Tower
from classes.projectile import Projectile
from classes.map import GameMap

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Tower Defense")
clock = pygame.time.Clock()

# Load level waves
with open("levels/level1.json") as f:
    level_data = json.load(f)
waves = level_data["waves"]

# Game objects
game_map = GameMap()
enemies = []
towers = []
projectiles = []

# Game state
base_health = BASE_HEALTH_START
cash = START_CASH
wave_number = 0
current_wave_enemies = []
spawn_timer = 0
spawn_interval = 60

# Tower selection
selected_tower_type = "normal"
selected_tower = None

# Tower bar layout
tower_bar_start_x = WIDTH//2 - ((TOWER_BAR_WIDTH + TOWER_BAR_PADDING) * MAX_TOWER_SLOTS)//2
tower_bar_y = HEIGHT - TOWER_BAR_HEIGHT - 10
tower_bar_slots = ["normal", "sniper", "quick_attacker", None, None]

# Font
font = pygame.font.SysFont("arial", 20)

# ------------------- Functions -------------------
def start_next_wave():
    global wave_number, current_wave_enemies
    if wave_number < len(waves):
        current_wave_enemies = waves[wave_number][:]
        wave_number += 1

def create_enemy(enemy_type):
    return Enemy(game_map.path, enemy_type)

# ------------------- Main Loop -------------------
running = True
start_next_wave()

while running:
    clock.tick(FPS)
    WIN.fill(BLACK)

    # ---------------- Events ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # Left click -> select/place tower
            if event.button == 1:
                clicked_bar = False
                for i in range(MAX_TOWER_SLOTS):
                    slot_x = tower_bar_start_x + i * (TOWER_BAR_WIDTH + TOWER_BAR_PADDING)
                    rect = pygame.Rect(slot_x, tower_bar_y, TOWER_BAR_WIDTH, TOWER_BAR_HEIGHT)
                    tower_type = tower_bar_slots[i]
                    if rect.collidepoint(x, y) and tower_type:
                        if tower_type in TOWER_TYPES:
                            selected_tower_type = tower_type
                        clicked_bar = True
                        break
                if not clicked_bar:
                    # Check if clicked on tower
                    clicked_tower = None
                    for t in towers:
                        if (t.x - x)**2 + (t.y - y)**2 <= 15**2:
                            clicked_tower = t
                            break
                    if clicked_tower:
                        selected_tower = clicked_tower
                    else:
                        # Place tower
                        if selected_tower_type in TOWER_TYPES:
                            cost = TOWER_TYPES[selected_tower_type]["cost"]
                            if cash >= cost:
                                towers.append(Tower(x, y, selected_tower_type))
                                cash -= cost
                                selected_tower = None
            # Right click -> remove tower
            elif event.button == 3:
                for t in towers[:]:
                    if (t.x - x)**2 + (t.y - y)**2 <= 15**2:
                        towers.remove(t)
                        cash += TOWER_TYPES[t.type]["cost"] // 2  # Refund half
                        break

    # ---------------- Spawn enemies ----------------
    if current_wave_enemies:
        if spawn_timer <= 0:
            enemy_info = current_wave_enemies[0]
            enemies.append(create_enemy(enemy_info["type"]))
            enemy_info["count"] -= 1
            if enemy_info["count"] <= 0:
                current_wave_enemies.pop(0)
            spawn_timer = spawn_interval
        else:
            spawn_timer -= 1

    # ---------------- Update enemies ----------------
    for enemy in enemies[:]:
        enemy.move()
        if enemy.health <= 0:
            enemies.remove(enemy)
            cash += ENEMY_CASH.get(enemy.type, 10)
        elif enemy.path_index >= len(enemy.path) - 1:
            enemies.remove(enemy)
            base_health -= 1

    # ---------------- Update towers ----------------
    for tower in towers:
        tower.update(enemies, projectiles)

    # ---------------- Update projectiles ----------------
    for proj in projectiles[:]:
        proj.move()
        if proj.target.health <= 0 or proj.hit_target():
            projectiles.remove(proj)

    # ---------------- Next wave ----------------
    if not current_wave_enemies and len(enemies) == 0 and wave_number < len(waves):
        start_next_wave()

    # ---------------- Draw ----------------
    game_map.draw(WIN)

    for enemy in enemies:
        enemy.draw(WIN)
    for tower in towers:
        tower.draw(WIN, selected_tower)
    for proj in projectiles:
        proj.draw(WIN)

    # ---------------- UI ----------------
    base_text = font.render(f"Base Health: {base_health}", True, WHITE)
    wave_text = font.render(f"Wave: {wave_number}/{len(waves)}", True, WHITE)
    cash_text = font.render(f"Cash: ${cash}", True, WHITE)
    WIN.blit(base_text, (10, 10))
    WIN.blit(wave_text, (WIDTH - 150, 10))
    WIN.blit(cash_text, (WIDTH//2 - 50, 10))

    # ---------------- Tower Bar ----------------
    for i in range(MAX_TOWER_SLOTS):
        slot_x = tower_bar_start_x + i * (TOWER_BAR_WIDTH + TOWER_BAR_PADDING)
        rect = pygame.Rect(slot_x, tower_bar_y, TOWER_BAR_WIDTH, TOWER_BAR_HEIGHT)
        pygame.draw.rect(WIN, (50,50,50), rect)
        pygame.draw.rect(WIN, WHITE, rect, 2)
        tower_type = tower_bar_slots[i]
        if tower_type and tower_type in TOWER_TYPES:
            color = TOWER_TYPES[tower_type]["color"]
            pygame.draw.circle(WIN, color, (slot_x + TOWER_BAR_WIDTH//2, tower_bar_y + TOWER_BAR_HEIGHT//2), 20)
            cost_text = font.render(f"${TOWER_TYPES[tower_type]['cost']}", True, WHITE)
            WIN.blit(cost_text, (slot_x + 5, tower_bar_y + TOWER_BAR_HEIGHT - 20))
            if selected_tower_type == tower_type:
                pygame.draw.rect(WIN, YELLOW, rect, 3)

    # ---------------- Game Over ----------------
    if base_health <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        WIN.blit(game_over_text, (WIDTH//2 - 50, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()
