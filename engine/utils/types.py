import typing
from typing import runtime_checkable

RelativeCoord = typing.Annotated[float, "range: 0-1"]
RelativeCoords = tuple[RelativeCoord, RelativeCoord]

BasicFunction = typing.Callable[..., None]


@runtime_checkable
class Destroyable(typing.Protocol):
    def destroy(self) -> None:
        pass


@runtime_checkable
class BasicInstance(typing.Protocol):
    id: str
