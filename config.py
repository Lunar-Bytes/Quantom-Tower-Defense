# Window
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)  # for quick attacker

# Game settings
ENEMY_SPEED = 2
BASE_HEALTH_START = 10
START_CASH = 150

# Tower types
TOWER_TYPES = {
    "normal": {"cost": 50, "damage": 10, "range": 100, "cooldown": 60, "color": BLUE},
    "sniper": {"cost": 120, "damage": 30, "range": 200, "cooldown": 120, "color": PURPLE},
    "quick_attacker": {"cost": 75, "damage": 5, "range": 75, "cooldown": 15, "color": CYAN}
}

# Tower bar
MAX_TOWER_SLOTS = 5
TOWER_BAR_WIDTH = 60
TOWER_BAR_HEIGHT = 60
TOWER_BAR_PADDING = 10
