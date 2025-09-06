from typing import runtime_checkable, Protocol, Callable

EmptyFunction = Callable[..., None]

EasingFunction = Callable[[float], float]


@runtime_checkable
class Destroyable(Protocol):
    def destroy(self) -> None:
        pass
