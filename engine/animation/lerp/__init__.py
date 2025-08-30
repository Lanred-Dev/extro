import typing
import pygame
from .number import lerpNumber
from .color import lerpColor
from .vector import lerpVector
from engine.Console import console, LogType

LerpableType = typing.TypeVar(
    "LerpableType", float, int, pygame.Vector2, pygame.Vector3, pygame.Color
)


def lerp(start: LerpableType, end: LerpableType, progress: float) -> LerpableType:
    """Lerp between a start and end value at x."""
    if isinstance(start, pygame.Color) and isinstance(end, pygame.Color):
        return lerpColor(start, end, progress)
    elif (isinstance(start, pygame.Vector2) and isinstance(end, pygame.Vector2)) or (
        isinstance(start, pygame.Vector3) and isinstance(end, pygame.Vector3)
    ):
        return lerpVector(start, end, progress)
    elif isinstance(start, (float, int)) and isinstance(end, (float, int)):
        return type(start)(lerpNumber(start, end, progress))
    else:
        console.log(
            f"Unable to lerp value of type {type(start).__name__}",
            LogType.WARNING,
        )
        return start
