import pyray

import src.internal.Console as Console
from src.values.Vector2 import Vector2

_camera: "pyray.Camera2D | None" = None
world_tile_size: int = 30
camera_position: Vector2 = Vector2(0, 0)


def set_world_tile_size(size: int):
    global world_tile_size

    if size <= 0:
        Console.log("World tile size must be greater than 0", Console.LogType.ERROR)
        return

    world_tile_size = size
    Console.log(f"World tile size set to {world_tile_size}")


def _set_camera(camera: "pyray.Camera2D | None"):
    global _camera
    _camera = camera
    Console.log(
        "A new camera is being used for world rendering"
        if camera
        else "No camera is being used for world rendering"
    )


__all__ = [
    "_camera",
    "set_world_tile_size",
    "world_tile_size",
    "camera_position",
    "_set_camera",
]
