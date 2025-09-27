import typing
from extro.animation.lerp.number import lerpNumber
from extro.animation.lerp.color import lerpColor
from extro.animation.lerp.vector import lerpVector
from extro.values.Color import Color
from extro.values.Vector2 import Vector2

LerpableType = typing.TypeVar("LerpableType", float, int, Vector2, Color)


def lerp(start: LerpableType, end: LerpableType, progress: float) -> LerpableType:
    if isinstance(start, Color) and isinstance(end, Color):
        return lerpColor(start, end, progress)
    elif isinstance(start, Vector2) and isinstance(end, Vector2):
        return lerpVector(start, end, progress)
    elif isinstance(start, (float, int)) and isinstance(end, (float, int)):
        return type(start)(lerpNumber(start, end, progress))

    return start
