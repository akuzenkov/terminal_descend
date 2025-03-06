import logging
from time import time

from utils.primitives import Vector2D
from utils.collisions import Collider
from utils.scene import SceneManager


logger = logging.getLogger(__file__)


class GameObject:
    def __init__(self, pos, grid=None):
        self._pos = pos
        self.prev_pos = pos
        self.delta_pos = Vector2D(0, 0)

        self.screen_weight = float("inf")
        self.char = None

        self.created_at = time()
        self.is_updatable = True
        self.is_deleted = False
        
        self.scene_manager = SceneManager()
        self.grid = grid or self.scene_manager.grid

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, value):
        self.grid.remove_object(self)
        self._pos = value
        self.grid.add_object(self)

    def __setattr__(self, name, value):
        if isinstance(value, SceneManager):
            value.game_objects.send(self)

        if isinstance(value, Collider):
            value.linked_object = self
        
        super().__setattr__(name, value)

    def __hash__(self):
        return hash(id(self))
    
    def __eq__(self, other):
        return other is self
    
    def __repr__(self):
        return fr"{type(self)} in position {self.pos}"

    def start(self):
        pass
        
    def update(self):
        pass

    def destroy(self):
        self.is_deleted = True

    def on_collision(self, other):
        pass