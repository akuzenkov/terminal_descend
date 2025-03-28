import random
import logging
from collections import deque
from enum import Enum

import config

from utils.primitives import Vector2D
from utils.misc import LevelGenerator


logger = logging.getLogger(__file__)


class SceneType(Enum):
    EXPLORE = "EXPLORE"
    FIGHT = "FIGHT"

class GridManager:
    def __init__(self):
        self.explore_grids = self._coroutine()
        self.fight_grids = self._coroutine()

        next(self.explore_grids)
        next(self.fight_grids)

        self.scene_type = SceneType.EXPLORE

        self._yielded_objects = []
        self._is_switched = False

    def switch(self):
        for object in self._yielded_objects:
            self.send(object)

        self._yielded_objects.clear()

        self.scene_type = SceneType.EXPLORE if self.scene_type is SceneType.FIGHT else SceneType.FIGHT

    def _coroutine(self):
        q, value = deque([]), None
        while True:
            value = yield value
            if value:
                q.append(value)
            else:
                if q:
                    value = q.popleft()
                else:
                    value = None

    def send(self, object):
        if self.scene_type is SceneType.EXPLORE:
            self.explore_grids.send(object)
        else:
            self.fight_grids.send(object)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.scene_type is SceneType.EXPLORE:
            gen = self.explore_grids
        else:
            gen = self.fight_grids

        object = next(gen)

        if object is not None:
            self._yielded_objects.append(object)
            return object
        else:
            for object in self._yielded_objects:
                self.send(object)

            self._yielded_objects.clear()
            raise StopIteration
        
        
class GameObjectManager:
    def __init__(self):
        self.explore_game_objects = self._coroutine()
        self.fight_game_objects = self._coroutine()

        next(self.explore_game_objects)
        next(self.fight_game_objects)

        self.scene_type = SceneType.EXPLORE

        self._yielded_objects = []
        self._is_switched = False

    def switch(self):
        for object in self._yielded_objects:
                self.send(object)

        self._yielded_objects.clear()

        self.scene_type = SceneType.EXPLORE if self.scene_type is SceneType.FIGHT else SceneType.FIGHT

    def _coroutine(self):
        q, value = deque([]), None
        while True:
            value = yield value
            if value:
                q.append(value)
            else:
                if q:
                    value = q.popleft()
                else:
                    value = None

    def send(self, object):
        if not object.is_updatable:
            return
        
        if self.scene_type is SceneType.EXPLORE:
            self.explore_game_objects.send(object)
        else:
            self.fight_game_objects.send(object)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.scene_type is SceneType.EXPLORE:
            gen = self.explore_game_objects
        else:
            gen = self.fight_game_objects

        while True:
            object = next(gen)
            if object is None or not object.is_deleted:
                break

        if object is not None:
            self._yielded_objects.append(object)
            return object
        else:
            for object in self._yielded_objects:
                self.send(object)

            self._yielded_objects.clear()
            raise StopIteration


class SceneMeta(type):
    _singletons = {}

    def __call__(cls, *args, **kwargs):
        if cls not in type(cls)._singletons:
            type(cls)._singletons[cls] = super().__call__(*args, **kwargs)

        return type(cls)._singletons[cls]


class SceneManager(metaclass=SceneMeta):
    def __init__(self):
        self.screen = None

        self.explore_grid = None
        self.explore_player = None
        self.explore_camera = None

        self.fight_grid = None
        self.fight_player = None
        self.fight_camera = None
        self.projectile_manager = None

        self.game_objects = GameObjectManager()
        self.grids = GridManager()
        self.scene_type = SceneType.EXPLORE

        self.player_cls, self.camera_cls, self.wall_cls, self.floor_cls = None, None, None, None 
        self.projectile_manager_cls, self.enemy_cls, self.grid_cls = None, None, None

    def spawn_explore_scene(self):
        self.explore_grid = self.grid_cls(height=config.GRID_SIZE, width=config.GRID_SIZE)
        level_gen = LevelGenerator(self.explore_grid, self.wall_cls, self.floor_cls)
        level_gen.generate()

        while True:
            i, j = random.randint(0, config.GRID_SIZE - 1), random.randint(0, config.GRID_SIZE - 1)
            _, _, tile = self.explore_grid[i][j][0]
            if isinstance(tile, self.floor_cls):
                self.explore_player = self.player_cls(Vector2D(i, j), self.explore_grid)
                break
        
        self.enemy_cls(Vector2D(i, j + 1), self.explore_grid)

        self.explore_camera = self.camera_cls(Vector2D(0, 0), self.explore_grid, config.CAMERA_HEIGHT, config.CAMERA_WIDTH, config.FOCUS_DISTANCE)
        self.explore_camera.linked_object = self.explore_player
        self.explore_grid.camera = self.explore_camera

    def spawn_fight_scene(self, enemy):
        self.fight_grid = self.grid_cls(height=config.FIGHT_GRID_SIZE, width=config.FIGHT_GRID_SIZE, terminal_pos=Vector2D(20, 20))
        level_gen = LevelGenerator(self.fight_grid, self.wall_cls, self.floor_cls)
        level_gen.generate_empty()

        self.projectile_manager = self.projectile_manager_cls(Vector2D(0, 0), enemy, self.fight_grid)

        self.health_grid = self.grid_cls(height=2, width=40, terminal_pos=Vector2D(10, 0))
        self.health_grid.camera = self.camera_cls(Vector2D(0, 0), self.health_grid, height=2, width=40, focus=0)
        level_generator = LevelGenerator(self.health_grid, self.wall_cls, self.floor_cls)
        level_generator.generate_one_row()
        fight_enemy = type(enemy)(Vector2D(0, 0), self.health_grid)


        while True:
            i, j = random.randint(0, config.FIGHT_GRID_SIZE - 1), random.randint(0, config.FIGHT_GRID_SIZE - 1)
            _, _, tile = self.fight_grid[i][j][0]
            if isinstance(tile, self.floor_cls):
                self.fight_player = self.player_cls(Vector2D(i, j))
                break

        self.fight_camera = self.camera_cls(Vector2D(0, 0), self.fight_grid, config.FIGHT_CAMERA_HEIGHT, config.FIGHT_CAMERA_WIDTH, config.FIGHT_FOCUS_DISTANCE)
        self.fight_camera.linked_object = self.fight_player
        self.fight_grid.camera = self.fight_camera

    def switch(self, enemy=None):
        self.screen.clear()

        if self.scene_type is SceneType.EXPLORE:
            self.game_objects.switch()
            self.grids.switch()

            self.scene_type = SceneType.FIGHT
            self.spawn_fight_scene(enemy)
        else:
            self.game_objects.switch()
            self.grids.switch()
            self.scene_type = SceneType.EXPLORE
            

    @property
    def grid(self):
        if self.scene_type is SceneType.EXPLORE:
            return self.explore_grid
        else:
            return self.fight_grid
        
    @property
    def player(self):
        if self.scene_type is SceneType.EXPLORE:
            return self.explore_player
        else:
            return self.fight_player
        
    @property
    def camera(self):
        if self.scene_type is SceneType.EXPLORE:
            return self.explore_camera
        else:
            return self.fight_camera


