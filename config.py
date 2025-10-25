# Window
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 150)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)

# Tower settings
TOWER_BAR_WIDTH = 60
TOWER_BAR_HEIGHT = 60
TOWER_BAR_PADDING = 10
MAX_TOWER_SLOTS = 5

TOWER_TYPES = {
    "normal": {"cost": 50, "damage": 5, "range": 100, "cooldown": 30, "color": BLUE},
    "sniper": {"cost": 150, "damage": 20, "range": 200, "cooldown": 60, "color": PURPLE},
    "quick_attacker": {"cost": 75, "damage": 10, "range": 75, "cooldown": 15, "color": YELLOW}
}

# Base
BASE_HEALTH_START = 20
START_CASH = 200

# Enemy
ENEMY_SPEED = 1
ENEMY_COLORS = {
    "basic": (0, 200, 0),
    "fast": (200, 200, 0),
    "tank": (200, 0, 0)
}

# Enemy cash reward
ENEMY_CASH = {
    "basic": 10,
    "fast": 15,
    "tank": 30
}
