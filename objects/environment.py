from objects.base import GameObject


class Floor(GameObject):
    is_updatable = False

    def __init__(self, pos, grid=None):
        super().__init__(pos, grid)

        self.screen_weight = float("inf")
        self.char = "   "


class Wall(GameObject):
    is_updatable = False

    def __init__(self, pos, grid=None):
        super().__init__(pos, grid)

        self.screen_weight = 0
        self.char = "\u2588\u2588\u2588"

