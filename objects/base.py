import logging

from utils.primitives import Vector2D
from utils.collisions import Collider
from utils.scene import SceneManager


logger = logging.getLogger(__file__)


class GameObject:
    def __init__(self, pos):
        self.scene_manager = SceneManager()

        self.prev_pos = pos
        self.delta_pos = Vector2D(0, 0)

        self.screen_weight = float("inf")

        self._pos = pos

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, value):
        self.scene_manager.grid.remove_object(self)
        self._pos = value
        self.scene_manager.grid.add_object(self)

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

    def on_collision(self, other):
        pass