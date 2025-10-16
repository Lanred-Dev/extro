from typing import Protocol, Callable

EmptyFunction = Callable[..., None]


class Destroyable(Protocol):
    def destroy(self) -> None:
        pass
