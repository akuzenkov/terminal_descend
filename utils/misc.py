import random

from utils.primitives import Vector2D


class LevelGenerator:
    #  Tile generator for explorational levels based on Cellular Automata principle.
    #  Genearates cave-like structures
    #TODO: Add region connectivity verification
    def __init__(self, grid, wall_cls, floor_cls):
        self.grid = grid
        self.wall_cls = wall_cls
        self.floor_cls = floor_cls
        
        self.wall_chance = 0.37
        self.to_wall_treshold = 5
        self.to_floor_treshold = 3
        self.iter_cnt = 3

    def init_field(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                cls = random.choices(
                    [self.wall_cls, self.floor_cls], 
                    [self.wall_chance, 1 - self.wall_chance]
                    )[0]
                
                cls(Vector2D(i, j), self.grid)
                
    def count_walls(self, i, j):
        wall_cnt = 0
        dirs = [
            [0, -1], [-1, -1], [-1, 0], [-1, 1],
            [0, 1], [1, 1], [1, 0], [1, -1]
            ]
        
        for d_i, d_j in dirs:
            nei_i, nei_j = i + d_i, j + d_j
            if nei_i < 0 or nei_i >= len(self.grid) or nei_j < 0 or nei_j >= len(self.grid[i]):
                wall_cnt += 1
            else:
                if isinstance(self.grid.get_object_to_display(nei_i, nei_j), self.wall_cls):
                    wall_cnt += 1
        return wall_cnt
    
    def process_field(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                wall_cnt = self.count_walls(i, j)
                object = self.grid.get_object_to_display(i, j)

                if isinstance(object, self.floor_cls) and wall_cnt >= self.to_wall_treshold:
                    # self.grid.remove_object(object)
                    object.destroy()
                    self.wall_cls(Vector2D(i, j), self.grid)
                elif isinstance(object, self.wall_cls) and wall_cnt >= self.to_floor_treshold:
                    continue
                else:
                    # self.grid.remove_object(object)
                    object.destroy()
                    self.floor_cls(Vector2D(i, j), self.grid)
                
    def generate(self):
        self.init_field()
        for _ in range(self.iter_cnt):
            self.process_field()

    def generate_empty(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.floor_cls(Vector2D(i, j), self.grid)

    def generate_one_row(self):
        for j in range(len(self.grid[0])):
            self.wall_cls(Vector2D(0, j), self.grid)