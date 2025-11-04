"""Provides configuration for the game world, including the active camera and tile size."""

from typing import TYPE_CHECKING

import extro.Console as Console
from extro.shared.Vector2C import Vector2

if TYPE_CHECKING:
    from extro.instances.core.Camera import Camera


_DEFAULT_TILE_SIZE: Vector2 = Vector2(30, 30)

camera: "Camera | None" = None
tile_size: Vector2 = _DEFAULT_TILE_SIZE


def set_tile_size(size: Vector2 | float | int):
    """Set the world's tile size."""
    if isinstance(size, (int, float)):
        size = Vector2(size, size)

    if size <= Vector2(0, 0):
        Console.log(f"`tile_size` must be >0 (tried {size})", Console.LogType.ERROR)
        return

    global tile_size
    tile_size.x = size.x
    tile_size.y = size.y
    Console.log(f"`tile_size` set to {size}")


def set_camera(new_camera: "Camera | None"):
    """
    Set the world's active camera. Rendering will follow this camera.

    If None, then the top-left corner will be (0, 0) in world coordinates.
    """
    global camera
    camera = new_camera
    Console.log(
        f"World camera set to {"new camera" if new_camera else "None"}",
        Console.LogType.DEBUG,
    )


__all__ = [
    "tile_size",
    "set_tile_size",
    "camera",
    "set_camera",
]
