import random
import logging
from collections import deque
from enum import Enum

import config

from utils.primitives import Vector2D
from utils.grid import Grid
from utils.misc import LevelGenerator


logger = logging.getLogger(__file__)


class SceneType(Enum):
    EXPLORE = "EXPLORE"
    FIGHT = "FIGHT"


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

        object = next(gen)

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

        self.game_objects = GameObjectManager()
        self.scene_type = SceneType.EXPLORE

        self.player_cls, self.camera_cls, self.wall_cls, self.floor_cls = None, None, None, None 

    def spawn_explore_scene(self):
        self.explore_grid = Grid(height=config.GRID_SIZE, width=config.GRID_SIZE)
        level_gen = LevelGenerator(self.explore_grid, self.wall_cls, self.floor_cls)
        level_gen.generate()

        while True:
            i, j = random.randint(0, config.GRID_SIZE - 1), random.randint(0, config.GRID_SIZE - 1)
            _, tile = self.explore_grid[i][j][0]
            if isinstance(tile, self.floor_cls):
                self.explore_player = self.player_cls(Vector2D(i, j))
                break

        self.explore_camera = self.camera_cls(Vector2D(0, 0), config.CAMERA_HEIGHT, config.CAMERA_WIDTH, config.FOCUS_DISTANCE)
        self.explore_camera.linked_object = self.explore_player

    def spawn_fight_scene(self):
        self.fight_game_objects = []

        self.fight_grid = Grid(height=config.FIGHT_GRID_SIZE, width=config.FIGHT_GRID_SIZE)
        level_gen = LevelGenerator(self.fight_grid, self.wall_cls, self.floor_cls)
        level_gen.generate_empty()

        while True:
            i, j = random.randint(0, config.FIGHT_GRID_SIZE - 1), random.randint(0, config.FIGHT_GRID_SIZE - 1)
            _, tile = self.fight_grid[i][j][0]
            if isinstance(tile, self.floor_cls):
                self.fight_player = self.player_cls(Vector2D(i, j))
                break

        self.fight_camera = self.camera_cls(Vector2D(0, 0), config.FIGHT_CAMERA_HEIGHT, config.FIGHT_CAMERA_WIDTH, config.FIGHT_FOCUS_DISTANCE)
        self.fight_camera.linked_object = self.fight_player

    def switch(self):
        self.screen.clear()

        if self.scene_type is SceneType.EXPLORE:
            self.game_objects.switch()
            self.scene_type = SceneType.FIGHT
            self.spawn_fight_scene()
        else:
            self.game_objects.switch()
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


