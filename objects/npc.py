from objects.base import GameObject
from utils.primitives import Vector2D

class Enemy(GameObject):
    def __init__(self, pos):
        super().__init__(pos)

        self.dir = Vector2D(0, 1)
        self.speed = 1
