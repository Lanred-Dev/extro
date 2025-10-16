from extro.animation.lerp.number import lerpNumber
from extro.shared.Vector2C import Vector2


def lerpVector(start: Vector2, end: Vector2, progress: float) -> Vector2:
    return Vector2(
        lerpNumber(start.x, end.x, progress), lerpNumber(start.y, end.y, progress)
    )
