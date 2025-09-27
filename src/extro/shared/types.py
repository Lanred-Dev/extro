from typing import Protocol, Callable, TypeVar, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from extro.shared import Vector2, Color

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
