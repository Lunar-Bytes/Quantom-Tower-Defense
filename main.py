import pygame
import sys
import json
import os
from config import *
from classes.enemy import Enemy
from classes.tower import Tower
from classes.projectile import Projectile
from classes.map import GameMap
from level_select import level_select_screen, save_progress, progress

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Tower Defense")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# === Load level ===
def load_level(level_file):
    with open(level_file) as f:
        return json.load(f)["waves"]

selected_level_file = level_select_screen()
if selected_level_file is None:
    pygame.quit()
    sys.exit()

waves = load_level(selected_level_file)

# === Game objects ===
game_map = GameMap()
enemies = []
towers = []
projectiles = []

# === Game state ===
base_health = BASE_HEALTH_START
cash = START_CASH
wave_number = 0
current_wave_enemies = []
spawn_timer = 0
spawn_interval = 60
current_wave_bonus = 0

# Tower selection
selected_tower_type = "normal"
selected_tower = None

# Tower bar layout
tower_bar_start_x = WIDTH // 2 - ((TOWER_BAR_WIDTH + TOWER_BAR_PADDING) * MAX_TOWER_SLOTS) // 2
tower_bar_y = HEIGHT - TOWER_BAR_HEIGHT - 10
tower_bar_slots = ["normal", "sniper", "quick_attacker", None, None]

# === Functions ===
def start_next_wave():
    global wave_number, current_wave_enemies, current_wave_bonus
    if wave_number < len(waves):
        wave = waves[wave_number]
        current_wave_enemies = []
        current_wave_bonus = 0
        for enemy_info in wave:
            if "type" in enemy_info:
                current_wave_enemies.append(enemy_info.copy())
            elif "reward" in enemy_info:
                current_wave_bonus = int(enemy_info["reward"])
        wave_number += 1

def create_enemy(enemy_type, path):
    return Enemy(path, enemy_type)

start_next_wave()

# === Main loop ===
running = True
while running:
    clock.tick(FPS)
    WIN.fill(BLACK)

    # Draw path
    if game_map.path:
        pygame.draw.lines(WIN, (200, 200, 200), False, game_map.path, 5)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Tower placement / removal
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if event.button == 3:
                for t in towers:
                    if (t.x - x)**2 + (t.y - y)**2 <= 15**2:
                        towers.remove(t)
                        break
            elif event.button == 1:
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
                    clicked_tower = None
                    for t in towers:
                        if (t.x - x)**2 + (t.y - y)**2 <= 15**2:
                            clicked_tower = t
                            break
                    if clicked_tower:
                        selected_tower = clicked_tower
                    else:
                        if selected_tower_type in TOWER_TYPES:
                            cost = TOWER_TYPES[selected_tower_type]["cost"]
                            if cash >= cost:
                                towers.append(Tower(x, y, selected_tower_type))
                                cash -= cost
                                selected_tower = None

    # --- Spawn enemies ---
    if current_wave_enemies:
        if spawn_timer <= 0:
            enemy_info = current_wave_enemies[0]
            enemies.append(create_enemy(enemy_info["type"], game_map.path))
            enemy_info["count"] -= 1
            if enemy_info["count"] <= 0:
                current_wave_enemies.pop(0)
            spawn_timer = spawn_interval
        else:
            spawn_timer -= 1

    # --- Update enemies ---
    for enemy in enemies[:]:
        enemy.move()
        if enemy.health <= 0:
            enemies.remove(enemy)
            cash += ENEMY_REWARD.get(enemy.enemy_type, 10)
        elif enemy.path_index >= len(enemy.path) - 1:
            enemies.remove(enemy)
            base_health -= 1

    # --- Update towers ---
    for tower in towers:
        tower.update(enemies, projectiles)

    # --- Update projectiles ---
    for proj in projectiles[:]:
        proj.move()
        if proj.target.health <= 0 or proj.hit_target():
            projectiles.remove(proj)

    # --- Next wave / level complete ---
    if not current_wave_enemies and not enemies:
        cash += current_wave_bonus
        if wave_number < len(waves):
            start_next_wave()
        else:
            # Level complete
            WIN.fill(BLACK)
            win_text = font.render("YOU WIN!", True, (0, 255, 0))
            WIN.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(4000)

            # Unlock next level
            level_files = sorted([f for f in os.listdir("levels") if f.endswith(".json")])
            current_level_name = os.path.basename(selected_level_file)
            idx = level_files.index(current_level_name)
            if idx + 1 < len(level_files):
                next_level = level_files[idx + 1]
                if next_level not in progress["unlocked_levels"]:
                    progress["unlocked_levels"].append(next_level)
                    save_progress()

            # Back to level select
            selected_level_file = level_select_screen()
            if selected_level_file is None:
                running = False
                break

            # Reset game state
            waves = load_level(selected_level_file)
            base_health = BASE_HEALTH_START
            cash = START_CASH
            wave_number = 0
            current_wave_enemies.clear()
            spawn_timer = 0
            enemies.clear()
            towers.clear()
            projectiles.clear()
            start_next_wave()

    # --- Draw map ---
    game_map.draw(WIN)

    # Draw enemies
    for enemy in enemies:
        enemy.draw(WIN)
        bar_width, bar_height = 20, 4
        health_ratio = enemy.health / enemy.max_health
        pygame.draw.rect(WIN, RED, (enemy.x - bar_width // 2, enemy.y - 20, bar_width, bar_height))
        color = ENEMY_COLORS.get(enemy.enemy_type, WHITE)
        pygame.draw.rect(WIN, color, (enemy.x - bar_width // 2, enemy.y - 20, int(bar_width * health_ratio), bar_height))

    # Draw towers
    for tower in towers:
        tower.draw(WIN, selected_tower)

    # Draw projectiles
    for proj in projectiles:
        proj.draw(WIN)

    # --- Draw UI ---
    base_text = font.render(f"Base Health: {base_health}", True, WHITE)
    wave_text = font.render(f"Wave: {wave_number}/{len(waves)}", True, WHITE)
    cash_text = font.render(f"Cash: ${cash}", True, WHITE)
    WIN.blit(base_text, (10, 10))
    WIN.blit(wave_text, (WIDTH - 150, 10))
    WIN.blit(cash_text, (WIDTH // 2 - 50, 10))

    # Tower bar
    for i in range(MAX_TOWER_SLOTS):
        slot_x = tower_bar_start_x + i * (TOWER_BAR_WIDTH + TOWER_BAR_PADDING)
        rect = pygame.Rect(slot_x, tower_bar_y, TOWER_BAR_WIDTH, TOWER_BAR_HEIGHT)
        pygame.draw.rect(WIN, (50, 50, 50), rect)
        pygame.draw.rect(WIN, WHITE, rect, 2)
        tower_type = tower_bar_slots[i]
        if tower_type and tower_type in TOWER_TYPES:
            color = TOWER_TYPES[tower_type]["color"]
            pygame.draw.circle(WIN, color, (slot_x + TOWER_BAR_WIDTH // 2, tower_bar_y + TOWER_BAR_HEIGHT // 2), 20)
            cost_text = font.render(f"${TOWER_TYPES[tower_type]['cost']}", True, WHITE)
            WIN.blit(cost_text, (slot_x + 5, tower_bar_y + TOWER_BAR_HEIGHT - 20))
            if selected_tower_type == tower_type:
                pygame.draw.rect(WIN, (255, 215, 0), rect, 3)

    # Game over
    if base_health <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        WIN.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()
