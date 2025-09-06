from src.animation.lerp.number import lerpNumber
from src.values.Vector2 import Vector2


def lerpVector(start: Vector2, end: Vector2, progress: float) -> Vector2:
    """Lerp between a start vector and end vector at x."""
    return Vector2(
        lerpNumber(start.x, end.x, progress), lerpNumber(start.y, end.y, progress)
    )
