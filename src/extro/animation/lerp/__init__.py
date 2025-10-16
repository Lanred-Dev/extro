from typing import TypeVar

from extro.animation.lerp.number import lerpNumber
from extro.animation.lerp.color import lerpColor
from extro.animation.lerp.vector import lerpVector
from extro.shared.Vector2C import Vector2
from extro.shared.RGBAColorC import RGBAColor

LerpableType = TypeVar("LerpableType", float, int, Vector2, RGBAColor)


def lerp(start: LerpableType, end: LerpableType, progress: float) -> LerpableType:
    if isinstance(start, RGBAColor) and isinstance(end, RGBAColor):
        return lerpColor(start, end, progress)
    elif isinstance(start, Vector2) and isinstance(end, Vector2):
        return lerpVector(start, end, progress)
    elif isinstance(start, (float, int)) and isinstance(end, (float, int)):
        return type(start)(lerpNumber(start, end, progress))

    return start
