from typing import Callable, TYPE_CHECKING

from extro.animation.easings.linear import linear

if TYPE_CHECKING:
    EasingFunction = Callable[[float], float]

__all__ = ["linear"]
