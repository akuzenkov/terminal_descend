import logging
from time import time

import config

from objects.base import GameObject
from objects.projectiles import Projectile
from objects.misc import Camera
from objects.environment import Wall, Floor

from utils.primitives import Vector2D
from utils.grid import Grid
from utils.misc import LevelGenerator
from utils.scene import SceneType


logger = logging.getLogger(__file__)


class Enemy(GameObject):
    def __init__(self, pos, grid=None):
        super().__init__(pos, grid)

        self.dir = Vector2D(0, 0)
        self.char = " X "
        self.screen_weight = -10

        self.pos = pos
        self.health = 10

        self.survived_time = 0
        self.time_to_survive = 5

        self.time_between_spawn = 1
        self.time_passed = 0

    def update(self):
        if self.scene_manager.scene_type is SceneType.FIGHT:
            self.survived_time += config.FRAME_DELTA_TIME      

    def fight_pattern(self, fight_grid):
        #  ZIG-ZAG pattern
        char, dir =  " \u2B07 ", Vector2D(1, 0)   # Down
        skip_cells, delta = [0, 1] , -1
        yield

        while True:
            for j in range(self.scene_manager.grid.width):
                if j in skip_cells:
                    continue
                
                Projectile(Vector2D(0, j), fight_grid, dir, char)
            
            if skip_cells[0] == 0 or skip_cells[-1] == fight_grid.width - 1:
                delta *= -1

            skip_cells[0] += delta
            skip_cells[-1] += delta

            self.time_passed = 0
            yield

    @property
    def avatar(self):
        return """
                          .-=-.          .--.  
              __        .'     '.       /  " ) 
      _     .'  '.     /   .-.   \     /  .-'\ 
     ( \   / .-.  \   /   /   \   \   /  /    ^
      \ `-` /   \  `-'   /     \   `-`  /      
       `-.-`     '.____.'       `.____.'       
"""