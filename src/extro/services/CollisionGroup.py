"""Provides collision group management for collision and physics interactions."""

import extro.Console as Console

DEFAULT_COLLISION_GROUP: str = "default"

_collision_matrix: dict[str, dict[str, bool]] = {DEFAULT_COLLISION_GROUP: {}}


def create_collision_group(collision_group: str):
    """Create a new collision group. By default, unless specified otherwise in `set_collidable`, all collision groups are collidable with each other."""
    if collision_group in _collision_matrix:
        Console.log(
            f"Collision group '{collision_group}' already exists",
            Console.LogType.WARNING,
        )
        return

    _collision_matrix[collision_group] = {}
    Console.log(f"Collision group '{collision_group}' created", Console.LogType.DEBUG)


def set_collidable(collision_group1: str, collision_group2: str, collidable: bool):
    """Set whether two collision groups are collidable with each other."""
    # Technically not creating a collision group before setting collidability is fine, but to enforce good practices its required
    if collision_group1 not in _collision_matrix:
        Console.log(
            f"Collision group '{collision_group1}' does not exist",
            Console.LogType.ERROR,
        )
        return
    elif collision_group2 not in _collision_matrix:
        Console.log(
            f"Collision group '{collision_group2}' does not exist",
            Console.LogType.ERROR,
        )
        return

    _collision_matrix[collision_group1][collision_group2] = collidable
    _collision_matrix[collision_group2][collision_group1] = collidable
    Console.log(
        f"Collision group '{collision_group1}' is {'now' if collidable else 'no longer'} collidable with '{collision_group2}'",
        Console.LogType.DEBUG,
    )


def is_collidable(collision_group1: str, collision_group2: str) -> bool:
    """Check if two collision groups are collidable with each other."""
    # No error is thrown because if a collision group doesn't exist, it can't collide with anything. Im also lazy and dont feel like adding error handling here :)
    if (
        collision_group1 not in _collision_matrix
        or collision_group2 not in _collision_matrix
    ):
        return False

    return _collision_matrix[collision_group1].get(
        collision_group2, True
    ) and _collision_matrix[collision_group2].get(collision_group1, True)


def is_group(group: str) -> bool:
    """Check if a collision group exists."""
    return group in _collision_matrix


__all__ = [
    "DEFAULT_COLLISION_GROUP",
    "create_collision_group",
    "set_collidable",
    "is_collidable",
    "is_group",
]
