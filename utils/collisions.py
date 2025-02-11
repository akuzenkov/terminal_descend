import logging


logger = logging.getLogger(__file__)


COLLIDER_OBJECTS = set()


class CollisionManager:
    @classmethod
    def process_collisions(cls, scene_manager):
        for object in scene_manager.game_objects:
            if object not in COLLIDER_OBJECTS:
                continue

            i, j = object.pos

            for _, grid_object in scene_manager.grid[i][j]:
                if object is grid_object:
                    continue

                object.on_collision(grid_object)


class Collider:
    def __init__(self):
        self._linked_object = None
        
    @property
    def linked_object(self):
        return self._linked_object
    
    @linked_object.setter
    def linked_object(self, value):
        COLLIDER_OBJECTS.discard(self._linked_object)
        self._linked_object = value
        COLLIDER_OBJECTS.add(self._linked_object)