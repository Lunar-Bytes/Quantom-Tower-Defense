# Window
WIDTH = 800
HEIGHT = 600
FPS = 60

# Game
BASE_HEALTH_START = 20
START_CASH = 200

# Tower bar
MAX_TOWER_SLOTS = 5
TOWER_BAR_WIDTH = 60
TOWER_BAR_HEIGHT = 60
TOWER_BAR_PADDING = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Tower definitions
TOWER_TYPES = {
    "normal": {"cost": 50, "damage": 5, "range": 100, "cooldown": 30, "color": BLUE},
    "sniper": {"cost": 150, "damage": 20, "range": 200, "cooldown": 90, "color": PURPLE},
    "quick_attacker": {"cost": 75, "damage": 10, "range": 75, "cooldown": 15, "color": GREEN}
}

# Enemy defaults
ENEMY_COLORS = {
    "basic": (255, 255, 255),
    "fast": (0, 255, 255),
    "tank": (255, 165, 0)
}

ENEMY_SPEEDS = {
    "basic": 1.0,
    "fast": 2.0,
    "tank": 0.5
}
