from typing import TYPE_CHECKING, TypeVar
from src.animation.easings import easings
from src.animation.Tween import TweenState, Tween

if TYPE_CHECKING:
    from src.values.Color import Color
    from src.values.Vector2 import Vector2

LerpableType = TypeVar("LerpableType", float, int, "Vector2", "Color")

__all__ = ["Tween", "TweenState", "easings", "LerpableType"]
