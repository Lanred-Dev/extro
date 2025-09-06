import typing
from src.animation.lerp.number import lerpNumber
from src.animation.lerp.color import lerpColor
from src.animation.lerp.vector import lerpVector
from src.internal.Console import Console, LogType
from src.values.Color import Color
from src.values.Vector2 import Vector2

LerpableType = typing.TypeVar("LerpableType", float, int, Vector2, Color)


def lerp(start: LerpableType, end: LerpableType, progress: float) -> LerpableType:
    """Lerp between a start and end value at x."""
    if isinstance(start, Color) and isinstance(end, Color):
        return lerpColor(start, end, progress)
    elif isinstance(start, Vector2) and isinstance(end, Vector2):
        return lerpVector(start, end, progress)
    elif isinstance(start, (float, int)) and isinstance(end, (float, int)):
        return type(start)(lerpNumber(start, end, progress))

    Console.log(
        f"{type(start).__name__} is not a lerpable value",
        LogType.WARNING,
    )

    return start
