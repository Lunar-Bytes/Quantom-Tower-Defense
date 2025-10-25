import pygame
import sys
import os
from config import *

def level_select_screen():
    # Determine base path for PyInstaller
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
    pygame.display.set_caption("Tower Defense")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("assets/fonts/arcade.ttf", 30)

    levels = [f for f in os.listdir(LEVEL_FOLDER) if f.endswith(".json")]
    levels.sort()

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50
    BUTTON_PADDING = 20
    buttons = []

    start_y = 100
    for i, level_file in enumerate(levels):
        x = WIDTH // 2 - BUTTON_WIDTH // 2
        y = start_y + i * (BUTTON_HEIGHT + BUTTON_PADDING)
        buttons.append({"rect": pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT), "file": level_file})

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
                for button in buttons:
                    if button["rect"].collidepoint(x, y):
                        selected_level = button["file"]
                        running = False
                        break

        for button in buttons:
            pygame.draw.rect(WIN, BLUE, button["rect"])
            pygame.draw.rect(WIN, WHITE, button["rect"], 3)
            text = font.render(button["file"].replace(".json", ""), True, WHITE)
            WIN.blit(text, (button["rect"].x + BUTTON_WIDTH//2 - text.get_width()//2,
                            button["rect"].y + BUTTON_HEIGHT//2 - text.get_height()//2))

        pygame.display.update()

    if selected_level is None:
        return None

    return os.path.join(LEVEL_FOLDER, selected_level)
