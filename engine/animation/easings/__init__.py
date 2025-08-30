import typing
from .linear import linear

EasingFunction = typing.Callable[[float], float]

__all__ = ["linear", "EasingFunction"]
