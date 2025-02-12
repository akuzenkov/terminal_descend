import logging

from time import time

import config
from input import keyboard
from objects.base import GameObject
from objects.environment import Wall
from utils.primitives import Vector2D
from utils.collisions import Collider


logger = logging.getLogger(__file__)


class Player(GameObject):
    def __init__(self, pos):
        super().__init__(pos)

        self.dir = Vector2D(0, 1)

        self.WALK_SPEED = 4
        self.speed = 4

        # Dash settings
        self.DASH_SPEED = 10
        self.is_dashing = False
        self.dash_time = 0.3
        self.dash_start_time = 0

        self.char = " @ "
        self.screen_weight = -999

    def start(self):
        self.collider = Collider()

    def update(self):
        directions = {
            "w": Vector2D(-1, 0),
            "a": Vector2D(0, -1),
            "s": Vector2D(1, 0),
            "d": Vector2D(0, 1)
        }

        key = keyboard.get_key()

        if self.is_dashing:
            if time() - self.dash_start_time >= self.dash_time:
                self.speed = self.WALK_SPEED
                self.is_dashing = False
        else:
            if key and key.char in directions:
                self.dir = directions[key.char]

            if key and key.char == "j" and not self.is_dashing:
                self.is_dashing = True
                self.speed = self.DASH_SPEED
                self.dash_start_time = time()

            if key and key.char == "f" and not self.is_dashing:
                self.scene_manager.switch()
                return

        # Because movement is tile-based and using int coordinats, 
        # to control speed of objects more precisely we need adjust decimal part of coords
        pos_offset = self.dir * self.speed * config.FRAME_DELTA_TIME    # Getting full position offset
        new_delta_pos = pos_offset - pos_offset.floor    # Extracting float part of offset
        self.delta_pos += new_delta_pos    # Increasing float part of offset between frames
        new_pos = self.pos + pos_offset.floor + self.delta_pos.floor    # Getting new int position
        self.delta_pos -= self.delta_pos.floor    # Extracting float part of offset

        # Updating position only if coords is range of GRID_SIZE
        if 0 <= new_pos.x < self.scene_manager.grid.height:
            new_prev_pos_x, new_pos_x = self.pos.x, new_pos.x
        else:
            new_prev_pos_x, new_pos_x = self.prev_pos.x, self.pos.x

        if 0 <= new_pos.y < self.scene_manager.grid.width:
            new_prev_pos_y, new_pos_y = self.pos.y, new_pos.y
        else:
            new_prev_pos_y, new_pos_y = self.prev_pos.y, self.pos.y

        self.prev_pos = Vector2D(new_prev_pos_x, new_prev_pos_y)
        self.pos = Vector2D(new_pos_x, new_pos_y)

    def on_collision(self, other):
        if isinstance(other, Wall):
            self.pos = self.prev_pos