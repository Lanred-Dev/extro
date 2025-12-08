"""Provides collision group management for collision and physics interactions."""

from typing import TYPE_CHECKING

import extro.Console as Console
import extro.internal.services.Identity as IdentityService

if TYPE_CHECKING:
    CollisionGroupID = int

DEFAULT_COLLISION_GROUP: str = "default"

_id_map: "dict[str, CollisionGroupID]" = {}
_collision_matrix: "dict[CollisionGroupID, dict[CollisionGroupID, bool]]" = {}


def create_group(collision_group: str) -> "CollisionGroupID | None":
    """Create a new collision group. By default, unless specified otherwise in `set_collidable`, all collision groups are collidable with each other."""
    if collision_group in _collision_matrix:
        Console.log(
            f"Collision group '{collision_group}' already exists",
            Console.LogType.WARNING,
        )
        return None

    id = IdentityService.generate_ordered_numeric_id()
    _id_map[collision_group] = id
    _collision_matrix[id] = {}
    Console.log(f"Created collision group '{collision_group}' with id {id}")

    # Need to set default collidability with existing groups
    for other_id in _collision_matrix:
        _collision_matrix[id][other_id] = True
        _collision_matrix[other_id][id] = True

    return id


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

    _collision_matrix[_id_map[collision_group1]][_id_map[collision_group2]] = collidable
    _collision_matrix[_id_map[collision_group2]][_id_map[collision_group1]] = collidable
    Console.log(
        f"Collision group '{collision_group1}' is {'now' if collidable else 'no longer'} collidable with '{collision_group2}'",
    )


def is_collidable(
    collision_group1: "CollisionGroupID", collision_group2: "CollisionGroupID"
) -> bool:
    """Check if two collision groups are collidable with each other."""
    return _collision_matrix[collision_group1][collision_group2]


def is_group(group: str) -> bool:
    """Check if a collision group exists."""
    return group in _id_map


def id_to_name(collision_group: "CollisionGroupID") -> str:
    """Convert a collision group ID to its corresponding name."""
    for name, id in _id_map.items():
        if id == collision_group:
            return name

    return ""


def name_to_id(collision_group: str) -> "CollisionGroupID":
    """Convert a collision group name to its corresponding ID."""
    return _id_map.get(collision_group, _id_map[DEFAULT_COLLISION_GROUP])


create_group(DEFAULT_COLLISION_GROUP)

__all__ = [
    "DEFAULT_COLLISION_GROUP",
    "create_group",
    "set_collidable",
    "is_collidable",
    "is_group",
    "id_to_name",
    "name_to_id",
]
