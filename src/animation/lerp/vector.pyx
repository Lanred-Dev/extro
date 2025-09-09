from src.animation.lerp.number import lerpNumber
from src.values.Vector2 import Vector2


cdef object lerpVector(object start, object end, float progress):
    return Vector2(
        lerpNumber(start.x, end.x, progress), lerpNumber(start.y, end.y, progress)
    )
