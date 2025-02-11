from objects.base import GameObject


class Tile:
    def __setattr__(self, name, value):        
        super().__setattr__(name, value)


class Floor(GameObject, Tile):
    def __init__(self, pos):
        super().__init__(pos)

        self.screen_weight = float("inf")
        self.char = "   "


class Wall(GameObject, Tile):
    def __init__(self, pos):
        super().__init__(pos)

        self.screen_weight = 0
        self.char = "\u2588\u2588\u2588"

