from typing import Protocol, Callable, TypeVar, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from src.values.Vector2 import Vector2
    from src.values.Color import Color

EmptyFunction = Callable[..., None]

EasingFunction = Callable[[float], float]

LerpableType = TypeVar("LerpableType", float, int, "Vector2", "Color")


class RenderTargetType(Enum):
    WORLD = 0
    INDEPENDENT = 1


class InstanceUpdateType(Enum):
    POSITION = 0
    SIZE = 1
    ROTATION = 2
    COLOR = 3


class Destroyable(Protocol):
    def destroy(self) -> None:
        pass
