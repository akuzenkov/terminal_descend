import logging

from objects.base import GameObject
from objects.projectiles import Projectile

from utils.primitives import Vector2D
from utils.grid import Grid


logger = logging.getLogger(__file__)


class Enemy(GameObject):
    def __init__(self, pos):
        super().__init__(pos)

        self.dir = Vector2D(0, 0)
        self.char = " X "
        self.screen_weight = -10

        self.pos = pos
        self.health = 10

        self.time_between_spawn = 1
        self.time_passed = 0
        # self.avatar_grid = Grid(height=10, width=10, terminal_pos=Vector2D(0, 20))

    def fight_pattern(self):
        #  ZIG-ZAG pattern
        char, dir =  " \u2B07 ", Vector2D(1, 0)   # Down
        skip_cells, delta = [0, 1] , -1
        yield

        while True:
            for j in range(self.scene_manager.grid.width):
                if j in skip_cells:
                    continue
                
                Projectile(Vector2D(0, j), dir, char)
            
            if skip_cells[0] == 0 or skip_cells[-1] == self.scene_manager.grid.width - 1:
                delta *= -1

            skip_cells[0] += delta
            skip_cells[-1] += delta

            self.time_passed = 0
            yield

    @property
    def pattern(self):
        return """
                          .-=-.          .--.  
              __        .'     '.       /  " ) 
      _     .'  '.     /   .-.   \     /  .-'\ 
     ( \   / .-.  \   /   /   \   \   /  /    ^
      \ `-` /   \  `-'   /     \   `-`  /      
       `-.-`     '.____.'       `.____.'       
"""