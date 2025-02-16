import logging
from pathlib import Path


FPS = 30
FRAME_DELTA_TIME = 1 / FPS

# Explore scene setting
GRID_SIZE = 200
CAMERA_HEIGHT = 40
CAMERA_WIDTH = 40
FOCUS_DISTANCE = 5

# Fight scene settings
FIGHT_GRID_SIZE = 10
FIGHT_CAMERA_HEIGHT = 10
FIGHT_CAMERA_WIDTH = 10
FIGHT_FOCUS_DISTANCE = 0

TERMINAL_HEIGHT = CAMERA_HEIGHT * 3
TERMINAL_WIDTH = CAMERA_WIDTH * 4


RUN_DIR = Path(__file__).absolute().parent
logging.basicConfig(filename=f"{RUN_DIR}/debug_logs.log", level=logging.DEBUG, format='%(asctime)s %(message)s')