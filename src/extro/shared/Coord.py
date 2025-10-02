from enum import Enum
from extro.shared.Vector2C import Vector2
import extro.services.Screen as ScreenService


class CoordType(Enum):
    NORMALIZED = 0
    ABSOLUTE = 1
    WORLD = 2
    RELATIVE = 3


class Coord(Vector2):
    absolute_x: float
    absolute_y: float
    type: CoordType

    def __init__(self, x=0.0, y=0.0, type=CoordType.NORMALIZED):
        super().__init__(x, y)

        self.type = type
        self.set(x, y)

    def to_tuple(self) -> tuple[float, float]:
        return (self.absolute_x, self.absolute_y)

    def set(self, new_x: float, new_y: float):
        match self.type:
            case CoordType.NORMALIZED:
                self.absolute_x, self.absolute_y = (
                    ScreenService.normalized_to_absolute_coords(new_x, new_y)
                )
            case CoordType.WORLD:
                self.absolute_x, self.absolute_y = (
                    ScreenService.world_to_absolute_coords(new_x, new_y)
                )
            case _:
                # ABSOLUTE and RELATIVE are assumed to not need conversion
                self.absolute_x = new_x
                self.absolute_y = new_y

    @Vector2.x.setter
    def x(self, value: float):
        self.set(value, self.y)

    @Vector2.y.setter
    def y(self, value: float):
        self.set(self.x, value)
