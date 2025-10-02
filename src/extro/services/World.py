"""Provides configuration for the game world, including the active camera and tile size."""

import extro.Console as Console
from extro.instances.core.Camera import Camera
from extro.shared.Vector2C import Vector2

_DEFAULT_CAMERA: Camera = Camera()
_DEFAULT_TILE_SIZE: Vector2 = Vector2(30, 30)

camera: Camera = _DEFAULT_CAMERA
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

    If None, then rendering will be centered on the origin of the world (0, 0).
    """
    global camera
    camera = new_camera if new_camera else _DEFAULT_CAMERA
    Console.log(
        f"World camera set to {new_camera if new_camera else "None"}",
        Console.LogType.DEBUG,
    )


__all__ = [
    "tile_size",
    "set_tile_size",
    "camera",
    "set_camera",
]
