import curses
import logging
from time import sleep

import config
from input.keyboard import Listener, on_press, on_release

from objects.projectiles import ProjectileManager
from objects.player import Player
from objects.environment import Wall, Floor
from objects.misc import Camera

from utils.collisions import CollisionManager
from utils.scene import SceneManager


logger = logging.getLogger(__name__)


def update(stdscr):
    curses.curs_set(0)
    stdscr.resize(config.TERMINAL_HEIGHT, config.TERMINAL_WIDTH)

    keyboard_listener = Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    scene_manager = SceneManager()
    scene_manager.screen = stdscr
    scene_manager.player_cls, scene_manager.camera_cls, scene_manager.wall_cls, scene_manager.floor_cls = Player, Camera, Wall, Floor
    scene_manager.projectile_manager_cls = ProjectileManager
    scene_manager.spawn_explore_scene()
    
    stdscr.clear()

    for object in scene_manager.game_objects:
        object.start()

    while True:
        for object in scene_manager.game_objects:
            object.update()

        CollisionManager.process_collisions(scene_manager)

        if scene_manager.camera.has_border:
            stdscr.addstr(0, 0, " * " * (scene_manager.camera.width + 2))
            line_num = 1
            for i in range(scene_manager.camera.c_tl_x, scene_manager.camera.c_br_x):
                line = [" * "]
                for j in range(scene_manager.camera.c_tl_y, scene_manager.camera.c_br_y):
                    object = scene_manager.grid.get_object_to_display(i, j)
                    line.append(object.char)
                line.append(" * ")

                stdscr.addstr(line_num, 0, "".join(line))
                line_num += 1

            stdscr.addstr(line_num, 0, " * " * (scene_manager.camera.width + 2))
        stdscr.refresh()

        sleep(config.FRAME_DELTA_TIME)


if __name__ == "__main__":
    curses.wrapper(update)