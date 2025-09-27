"""Provides functions for converting between world, screen, and normalized coordinate spaces."""

import random

import extro.Window as Window
from extro.shared.Vector2 import Vector2
import extro.services.World as WorldService


def normalized_to_screen_coords(vector: Vector2) -> Vector2:
    """Convert normalized coordinates (0 to 1) to screen coordinates."""
    return Vector2(vector.x * Window.size.x, vector.y * Window.size.y)


def world_to_screen_coords(vector: Vector2) -> Vector2:
    """Convert world coordinates to screen coordinates."""
    return Vector2(
        vector.x * WorldService.tile_size.x,
        vector.y * WorldService.tile_size.y,
    )


def screen_to_world_coords(vector: Vector2) -> Vector2:
    """Convert screen coordinates to world coordinates."""
    return Vector2(
        vector.x / WorldService.tile_size.x,
        vector.y / WorldService.tile_size.y,
    )


def random_world_coords(start: Vector2, end: Vector2) -> tuple[float, float]:
    """Generate random world coordinates within the specified bounds."""
    return (
        random.uniform(start.x, end.x),
        random.uniform(start.y, end.y),
    )


def random_screen_coords() -> tuple[float, float]:
    """Generate random screen coordinates within the current screen bounds."""
    return (random.uniform(0, Window.size.x), random.uniform(0, Window.size.y))


__all__ = [
    "normalized_to_screen_coords",
    "world_to_screen_coords",
    "screen_to_world_coords",
    "random_world_coords",
    "random_screen_coords",
]
