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

# ---------------- Editor Variables ----------------
editor_active = False
editor_waves = [wave.copy() for wave in waves]  # copy current waves
editor_current_wave = []
editor_selected_type = "basic"
editor_selected_count = 1
# --------------------------------------------------

# Start next wave
def start_next_wave():
    global wave_number, current_wave_enemies
    if wave_number < len(waves):
        current_wave_enemies = []
        for enemy_info in waves[wave_number]:
            current_wave_enemies.append(enemy_info.copy())
        wave_number += 1

start_next_wave()

# Create enemy based on type
def create_enemy(enemy_type, path=game_map.path):
    e = Enemy(path)
    if enemy_type == "fast":
        e.speed *= 1.5
        e.health = e.max_health = 20
    elif enemy_type == "tank":
        e.speed *= 0.7
        e.health = e.max_health = 50
    else:  # basic or others
        e.speed = 1
        e.health = e.max_health = 10
    return e

# ---------------- Editor Functions ----------------
def draw_editor():
    WIN.fill((40,40,40))
    y = 10
    WIN.blit(font.render(f"Wave Editor (CTRL+SHIFT+E to exit)", True, (255,255,255)), (10,y))
    y += 30
    WIN.blit(font.render(f"Selected Type: {editor_selected_type}  Count: {editor_selected_count}", True, (255,255,0)), (10,y))
    y += 30
    WIN.blit(font.render("Current Wave:", True, (180,180,180)), (10,y))
    y += 20
    for e in editor_current_wave:
        WIN.blit(font.render(f"{e['type']} x {e['count']}", True, (180,180,250)), (20, y))
        y += 20
    y += 10
    WIN.blit(font.render("Keys: 1-basic 2-fast 3-tank UP/DOWN-count A-add enemy N-new wave S-save", True, (200,200,200)), (10, HEIGHT-30))
    pygame.display.update()

def handle_editor_event(event):
    global editor_selected_type, editor_selected_count, editor_current_wave, editor_waves
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            editor_selected_type = "basic"
        elif event.key == pygame.K_2:
            editor_selected_type = "fast"
        elif event.key == pygame.K_3:
            editor_selected_type = "tank"
        elif event.key == pygame.K_UP:
            editor_selected_count += 1
        elif event.key == pygame.K_DOWN:
            editor_selected_count = max(1, editor_selected_count-1)
        elif event.key == pygame.K_a:
            editor_current_wave.append({"type": editor_selected_type, "count": editor_selected_count})
        elif event.key == pygame.K_n:
            if editor_current_wave:
                editor_waves.append(editor_current_wave)
                editor_current_wave = []
        elif event.key == pygame.K_s:
            if editor_current_wave:
                editor_waves.append(editor_current_wave)
            with open("levels/level1.json", "w") as f:
                json.dump({"waves": editor_waves}, f, indent=2)
            print("Saved level1.json")
            editor_waves = []
            editor_current_wave = []
# --------------------------------------------------

running = True
while running:
    clock.tick(FPS)

    keys = pygame.key.get_pressed()
    ctrl_shift_e = keys[pygame.K_LCTRL] and keys[pygame.K_LSHIFT] and keys[pygame.K_e]
    if ctrl_shift_e:
        editor_active = True

    if editor_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_editor_event(event)
            if event.type == pygame.KEYDOWN and ctrl_shift_e:
                editor_active = False  # exit editor
        draw_editor()
        continue  # skip game update while editor active

    WIN.fill((20, 20, 20))

    # ---------------- Events ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # Tower bar click
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
                # Place tower
                if selected_tower_type in TOWER_TYPES and cash >= TOWER_TYPES[selected_tower_type]["cost"]:
                    towers.append(Tower(x, y, selected_tower_type))
                    cash -= TOWER_TYPES[selected_tower_type]["cost"]
                    selected_tower = None

    # ---------------- Spawn enemies ----------------
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

    # ---------------- Update Enemies ----------------
    for enemy in enemies[:]:
        enemy.move()
        if enemy.health <= 0:
            enemies.remove(enemy)
            cash += {"basic":10, "fast":15, "tank":30}.get(enemy.type, 10)
        elif enemy.path_index >= len(enemy.path)-1:
            enemies.remove(enemy)
            base_health -= 1

    # ---------------- Update Towers ----------------
    for tower in towers:
        tower.update(enemies, projectiles)

    # ---------------- Update Projectiles ----------------
    for proj in projectiles[:]:
        proj.move()
        if proj.target.health <= 0 or proj.hit_target():
            projectiles.remove(proj)

    # Next wave
    if not current_wave_enemies and enemies == [] and wave_number < len(waves):
        start_next_wave()

    # ---------------- Draw ----------------
    game_map.draw(WIN)
    for enemy in enemies:
        enemy.draw(WIN)
    for tower in towers:
        tower.draw(WIN, selected_tower)
    for proj in projectiles:
        proj.draw(WIN)

    # UI
    WIN.blit(font.render(f"Base Health: {base_health}", True, WHITE), (10,10))
    WIN.blit(font.render(f"Wave: {wave_number}/{len(waves)}", True, WHITE), (WIDTH-150,10))
    WIN.blit(font.render(f"Cash: ${cash}", True, WHITE), (WIDTH//2 - 50,10))

    # Tower bar
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
                pygame.draw.rect(WIN, (255, 215, 0), rect, 3)

    # Game over
    if base_health <= 0:
        WIN.blit(font.render("GAME OVER", True, RED), (WIDTH//2-50, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()
