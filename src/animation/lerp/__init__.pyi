import typing
from src.values.Color import Color
from src.values.Vector2 import Vector2

LerpableType = typing.TypeVar("LerpableType", float, int, Vector2, Color)

def lerp(start: LerpableType, end: LerpableType, progress: float) -> LerpableType: ...
