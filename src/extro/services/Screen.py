"""Provides functions to convert between different coordinate systems and generate random coordinates."""

import random

from extro.shared.Vector2C import Vector2
import extro.services.World as WorldService
import extro.Window as Window


def normalized_to_absolute_coords(x: float, y: float) -> tuple[float, float]:
    return (x * Window.size.x, y * Window.size.y)


def absolute_to_normalized_coords(x: float, y: float) -> tuple[float, float]:
    return (x / Window.size.x, y / Window.size.y)


def world_to_absolute_coords(x: float, y: float) -> tuple[float, float]:
    return (x * WorldService.tile_size.x, y * WorldService.tile_size.y)


def absolute_to_world_coords(x: float, y: float) -> tuple[float, float]:
    return (x / WorldService.tile_size.x, y / WorldService.tile_size.y)


def random_coords_in_range(start: Vector2, end: Vector2) -> tuple[float, float]:
    return (random.uniform(start.x, end.x), random.uniform(start.y, end.y))


def random_absolute_coords() -> tuple[float, float]:
    return (random.uniform(0, Window.size.x), random.uniform(0, Window.size.y))


__all__ = [
    "normalized_to_absolute_coords",
    "absolute_to_normalized_coords",
    "world_to_absolute_coords",
    "absolute_to_world_coords",
    "random_coords_in_range",
    "random_absolute_coords",
]
