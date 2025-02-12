import logging

import config
from objects.base import GameObject
from utils.primitives import Vector2D


logger = logging.getLogger(__file__)


class Camera(GameObject):
    def __init__(self, pos, height, width, focus):
        super().__init__(pos)

        self.screen_weight = 1_000_000
        self.char = "   "

        self.height, self.width = height, width
        self.focus = focus

        self.linked_object = None

        self.c_tl_x, self.c_tl_y = self.pos.x, self.pos.y
        self.c_br_x, self.c_br_y = self.pos.x + self.height, self.pos.y + self.width
        self.f_tl_x, self.f_tl_y = self.pos.x + self.focus, self.pos.y + self.focus
        self.f_br_x, self.f_br_y = self.pos.x + self.height - self.focus, self.pos.y + self.width - self.focus

        self.has_border = True
    
    def update(self):
        if not self.linked_object:
            return

        new_pos_x, new_pos_y = self.pos
        # If linked_object out of scope of Camera, Camera center aligns by linked_object
        if any(
            (
                self.linked_object.pos.x < self.c_tl_x,
                self.linked_object.pos.x > self.c_br_x,
                self.linked_object.pos.y < self.c_tl_y,
                self.linked_object.pos.y > self.c_br_y
                )
        ):
            new_pos_x, new_pos_y = self.linked_object.pos.x - self.height // 2, self.linked_object.pos.y - self.width // 2

        # Moving Camera position if linked_object position is between Camera boundaries and focus boundaries
        if self.c_tl_x <= self.linked_object.pos.x <= self.f_tl_x:
            new_pos_x += self.linked_object.pos.x - self.f_tl_x 
        elif self.f_br_x <= self.linked_object.pos.x <= self.c_br_x:
            new_pos_x += self.linked_object.pos.x - self.f_br_x

        if self.c_tl_y <= self.linked_object.pos.y <= self.f_tl_y:
            new_pos_y += self.linked_object.pos.y - self.f_tl_y
        elif self.f_br_y <= self.linked_object.pos.y <= self.c_br_y:
            new_pos_y += self.linked_object.pos.y - self.f_br_y

        # Updating camera position only if coords is range of GRID_SIZE
        if not (0 <= new_pos_x and new_pos_x + self.height - 1 < self.scene_manager.grid.height):
            new_pos_x = self.pos.x

        if not (0 <= new_pos_y and new_pos_y + self.width - 1 < self.scene_manager.grid.width):
            new_pos_y = self.pos.y

        self.pos = Vector2D(new_pos_x, new_pos_y)

        # Updating camera boundaries and focus boundaries data
        self.c_tl_x, self.c_tl_y = self.pos.x, self.pos.y
        self.c_br_x, self.c_br_y = self.pos.x + self.height, self.pos.y + self.width
        self.f_tl_x, self.f_tl_y = self.pos.x + self.focus, self.pos.y + self.focus
        self.f_br_x, self.f_br_y = self.pos.x + self.height - self.focus, self.pos.y + self.width - self.focus
