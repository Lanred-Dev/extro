import typing
from src.animation.lerp.number import lerpNumber
from src.animation.lerp.color import lerpColor
from src.animation.lerp.vector import lerpVector
from src.values.Color import Color
from src.values.Vector2 import Vector2

cpdef object lerp(object start, object end, progress: float):
    """Lerp between a start and end value at x."""
    if isinstance(start, Color) and isinstance(end, Color):
        return lerpColor(start, end, progress)
    elif isinstance(start, Vector2) and isinstance(end, Vector2):
        return lerpVector(start, end, progress)
    elif isinstance(start, (float, int)) and isinstance(end, (float, int)):
        return type(start)(lerpNumber(start, end, progress))

