import pygame
import typing
from .number import lerpNumber

VectorType = typing.TypeVar("VectorType", pygame.Vector2, pygame.Vector3)


def lerpVector(start: VectorType, end: VectorType, progress: float) -> VectorType:
    """Lerp between a start vector and end vector at x."""

    vector = pygame.Vector2() if isinstance(start, pygame.Vector2) else pygame.Vector3()
    vector.x = lerpNumber(start.x, end.x, progress)
    vector.y = lerpNumber(start.y, end.y, progress)

    if (
        isinstance(start, pygame.Vector3)
        and isinstance(end, pygame.Vector3)
        and isinstance(vector, pygame.Vector3)
    ):
        vector.z = lerpNumber(start.z, end.z, progress)

    return typing.cast(VectorType, vector)
