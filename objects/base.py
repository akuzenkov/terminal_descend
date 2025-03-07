import logging
from time import time

from utils.primitives import Vector2D
from utils.collisions import Collider
from utils.scene import SceneManager


logger = logging.getLogger(__file__)


class GameObject:
    is_updatable = True
    is_deleted = False
    screen_weight = float("inf")

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)

        inst.is_updatable = cls.is_updatable
        inst.is_deleted = cls.is_deleted
        inst.screen_weight = cls.screen_weight
        inst.created_at = time()

        inst.scene_manager = SceneManager()

        return inst

    def __init__(self, pos, grid=None):
        self.grid = grid or self.scene_manager.grid

        self.pos = pos
        self.prev_pos = pos
        self.delta_pos = Vector2D(0, 0)

        self.char = None

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

        self.grid.remove_object(self)

    def on_collision(self, other):
        pass