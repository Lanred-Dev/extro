import math
from typing import List
from src.values.Vector2 import Vector2
from src.internal.components.DirtyUpdater import DirtyUpdater


def dot(a: Vector2, b: Vector2) -> float:
    """Dot product of two vectors."""
    return a.x * b.x + a.y * b.y


def subtract(a: Vector2, b: Vector2) -> Vector2:
    """Subtract vector b from a."""
    return Vector2(a.x - b.x, a.y - b.y)


def perpendicular(v: Vector2) -> Vector2:
    """Return a perpendicular vector (normal)."""
    return Vector2(-v.y, v.x)


def project_polygon(axis: Vector2, vertices: List[Vector2]) -> Vector2:
    """Project all vertices onto an axis and return min/max values."""
    dots = [dot(vertex, axis) for vertex in vertices]
    return Vector2(min(dots), max(dots))


def overlap(projection1: Vector2, projection2: Vector2) -> bool:
    """Check if two projections overlap."""
    return projection1.x <= projection2.y and projection2.x <= projection1.y


class CollisionMask(DirtyUpdater):
    position: Vector2
    size: Vector2
    rotation: float
    __vertices: List[Vector2]

    def __init__(self, position: Vector2, size: Vector2, rotation: float = 0):
        """
        x, y = center position
        width, height = size
        rotation = degrees
        """
        super().__init__()
        self.position = position
        self.size = size
        self.rotation = rotation
        self.__vertices = []
        self.mark_dirty(self.__compute_vertices)

    def set_size(self, size: Vector2):
        self.size = size
        self.mark_dirty(self.__compute_vertices)

    def set_position(self, position: Vector2):
        self.position = position
        self.mark_dirty(self.__compute_vertices)

    def set_rotation(self, rotation: int):
        self.rotation = rotation
        self.mark_dirty(self.__compute_vertices)

    def __compute_vertices(self):
        """Compute rectangle corners based on center, size, and rotation."""
        width, height = self.size.x / 2, self.size.y / 2
        radians = math.radians(self.rotation)

        local_vertices = [
            (-width, -height),
            (width, -height),
            (width, height),
            (-width, height),
        ]

        self.__vertices = [
            Vector2(
                self.position.x
                + vertex[0] * math.cos(radians)
                - vertex[1] * math.sin(radians),
                self.position.y
                + vertex[0] * math.sin(radians)
                + vertex[1] * math.cos(radians),
            )
            for vertex in local_vertices
        ]

    def get_axes(self) -> List[Vector2]:
        """Return the normals of edges for SAT."""

        axes = []

        for index in range(len(self.__vertices)):
            edge = subtract(
                self.__vertices[(index + 1) % len(self.__vertices)],
                self.__vertices[index],
            )
            axes.append(perpendicular(edge))

        return axes[:2]

    def get_vertices(self) -> List[Vector2]:
        self.recompute_if_needed()
        return self.__vertices

    def collides_with(self, other_collision_mask: "CollisionMask") -> bool:
        """Check collision with another OBB using SAT."""
        self.recompute_if_needed()

        axes = self.get_axes() + other_collision_mask.get_axes()

        for axis in axes:
            length = math.hypot(axis.x, axis.y)
            normal_axis = Vector2(axis.x / length, axis.y / length)
            projection1 = project_polygon(normal_axis, self.__vertices)
            projection2 = project_polygon(
                normal_axis, other_collision_mask.get_vertices()
            )

            if not overlap(projection1, projection2):
                return False

        return True
