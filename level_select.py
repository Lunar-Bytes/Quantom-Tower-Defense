import pygame
import sys
import os
from config import *
import json

PROGRESS_FILE = "levels/progress.json"

# Load or create progress file
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE) as f:
        progress = json.load(f)
else:
    progress = {"unlocked_levels": ["level1.json"]}

def save_progress():
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

def level_select_screen():
    # Determine base path
    if getattr(sys, 'frozen', False):
        BASE_PATH = sys._MEIPASS
    else:
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    LEVEL_FOLDER = os.path.join(BASE_PATH, "levels")
    if not os.path.exists(LEVEL_FOLDER):
        raise FileNotFoundError(f"Levels folder not found: {LEVEL_FOLDER}")

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Quantom Tower Defense")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("assets/fonts/arcade.ttf", 30)

    # Only show unlocked levels
    level_files = sorted([f for f in os.listdir(LEVEL_FOLDER) if f.endswith(".json")])
    unlocked = [lvl for lvl in level_files if lvl in progress["unlocked_levels"]]

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50
    BUTTON_PADDING = 20
    buttons = []

    start_y = 100
    for i, level_file in enumerate(unlocked):
        x = WIDTH // 2 - BUTTON_WIDTH // 2
        y = start_y + i * (BUTTON_HEIGHT + BUTTON_PADDING)
        buttons.append({"rect": pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT), "file": level_file})

    # Quit button top-left
    quit_button = {"rect": pygame.Rect(20, 20, 100, 40), "label": "QUIT"}

    selected_level = None
    running = True
    while running:
        clock.tick(FPS)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                # Check level buttons
                for button in buttons:
                    if button["rect"].collidepoint(x, y):
                        selected_level = button["file"]
                        running = False
                        break

                # Check quit button
                if quit_button["rect"].collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        # Draw level buttons
        for button in buttons:
            pygame.draw.rect(WIN, BLUE, button["rect"])
            pygame.draw.rect(WIN, WHITE, button["rect"], 3)
            text = font.render(button["file"].replace(".json", ""), True, WHITE)
            WIN.blit(text, (button["rect"].x + BUTTON_WIDTH // 2 - text.get_width() // 2,
                            button["rect"].y + BUTTON_HEIGHT // 2 - text.get_height() // 2))

        # Draw quit button
        pygame.draw.rect(WIN, RED, quit_button["rect"])
        pygame.draw.rect(WIN, WHITE, quit_button["rect"], 3)
        quit_text = font.render(quit_button["label"], True, WHITE)
        WIN.blit(quit_text, (quit_button["rect"].x + quit_button["rect"].width//2 - quit_text.get_width()//2,
                             quit_button["rect"].y + quit_button["rect"].height//2 - quit_text.get_height()//2))

        pygame.display.update()

    if selected_level is None:
        return None

    return os.path.join(LEVEL_FOLDER, selected_level)
