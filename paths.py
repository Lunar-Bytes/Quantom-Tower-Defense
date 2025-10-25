import sys
import os

# Determine base path for files
if getattr(sys, 'frozen', False):
    # Running as PyInstaller EXE
    BASE_PATH = sys._MEIPASS
else:
    # Running as normal Python script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

LEVEL_FOLDER = os.path.join(BASE_PATH, "levels")
ASSETS_FOLDER = os.path.join(BASE_PATH, "assets")