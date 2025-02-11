import logging
from pathlib import Path

from utils.grid import Grid


FPS = 60
FRAME_DELTA_TIME = 1 / FPS

GRID_SIZE = 200
FIGHT_GRID_SIZE = 25

CAMERA_HEIGHT = 40
CAMERA_WIDTH = 40
FOCUS_DISTANCE = 5

FIGHT_CAMERA_HEIGHT = 25
FIGHT_CAMERA_WIDTH = 25
FIGHT_FOCUS_DISTANCE = 0

TERMINAL_HEIGHT = CAMERA_HEIGHT * 3
TERMINAL_WIDTH = CAMERA_WIDTH * 3


RUN_DIR = Path(__file__).absolute().parent
logging.basicConfig(filename=f"{RUN_DIR}/debug_logs.log", level=logging.DEBUG, format='%(asctime)s %(message)s')