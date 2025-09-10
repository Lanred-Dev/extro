from typing import runtime_checkable, Protocol, Callable
from enum import Enum

EmptyFunction = Callable[..., None]

EasingFunction = Callable[[float], float]


class RenderTargetType(Enum):
    WORLD = 0
    INDEPENDENT = 1


@runtime_checkable
class Destroyable(Protocol):
    def destroy(self) -> None:
        pass
