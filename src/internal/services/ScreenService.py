import src.internal.Window as Window
from src.values.Vector2 import Vector2
import src.internal.services.WorldService as WorldService

screen_size: Vector2 = Window.size


def normalized_to_screen_coords(vector: Vector2) -> Vector2:
    return Vector2(vector.x * screen_size.x, vector.y * screen_size.y)


def world_to_screen_coords(vector: Vector2) -> Vector2:
    return Vector2(
        (vector.x - WorldService.camera_position.x) * WorldService.world_tile_size,
        (vector.y - WorldService.camera_position.y) * WorldService.world_tile_size,
    )


def screen_to_world_coords(vector: Vector2) -> Vector2:
    return Vector2(
        (vector.x / WorldService.world_tile_size) + WorldService.camera_position.x,
        (vector.y / WorldService.world_tile_size) + WorldService.camera_position.y,
    )


__all__ = [
    "screen_size",
    "normalized_to_screen_coords",
    "world_to_screen_coords",
    "screen_to_world_coords",
]
