from objects.base import GameObject


class Floor(GameObject):
    def __init__(self, pos):
        super().__init__(pos)

        self.is_updatable = False
        self.screen_weight = float("inf")
        self.char = "   "


class Wall(GameObject):
    def __init__(self, pos):
        super().__init__(pos)

        self.is_updatable = False
        self.screen_weight = 0
        self.char = "\u2588\u2588\u2588"

