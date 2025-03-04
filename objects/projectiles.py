import random
import logging

import config

from objects.base import GameObject
from utils.primitives import Vector2D


logger = logging.getLogger(__file__)


class ProjectileManager(GameObject):
    def __init__(self, pos, enemy):
        super().__init__(pos)

        self.screen_weight = 10_000_000

        self.enemy = enemy
        self.gen = enemy.fight_pattern()

    def update(self):
        if self.enemy.time_passed < self.enemy.time_between_spawn:
            self.enemy.time_passed += config.FRAME_DELTA_TIME
        else:
            next(self.gen)


class Projectile(GameObject):
    def __init__(self, pos, dir, char):
        super().__init__(pos)
        
        self.dir = dir
        self.char = char
        
        self.screen_weight = 1_000
        self.speed = 2

    def update(self):
        # Because movement is tile-based and using int coordinats, 
        # to control speed of objects more precisely we need adjust decimal part of coords
        pos_offset = self.dir * self.speed * config.FRAME_DELTA_TIME    # Getting full position offset
        new_delta_pos = pos_offset - pos_offset.floor                   # Extracting float part of offset
        self.delta_pos += new_delta_pos                                 # Increasing float part of offset between frames
        new_pos = self.pos + pos_offset.floor + self.delta_pos.floor    # Getting new int position
        self.delta_pos -= self.delta_pos.floor                          # Extracting float part of offset

        # Updating position only if coords is range of GRID_SIZE
        if 0 <= new_pos.x < self.scene_manager.grid.height:
            new_prev_pos_x, new_pos_x = self.pos.x, new_pos.x
        else:
            self.destroy()
            return

        if 0 <= new_pos.y < self.scene_manager.grid.width:
            new_prev_pos_y, new_pos_y = self.pos.y, new_pos.y
        else:
            self.destroy()
            return

        self.prev_pos = Vector2D(new_prev_pos_x, new_prev_pos_y)
        self.pos = Vector2D(new_pos_x, new_pos_y)


