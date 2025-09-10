from typing import List
from src.values.Vector2 import Vector2

class CollisionMask:
    position: Vector2
    size: Vector2
    rotation: float
    vertices: List[Vector2]
    axes: List[Vector2]

    def __init__(self, position: Vector2, size: Vector2, rotation: float = 0): ...
    def collides_with(self, other_collision_mask: CollisionMask) -> bool: ...
