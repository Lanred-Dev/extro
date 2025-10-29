from enum import Enum
from extro.shared.Vector2C import Vector2
import extro.services.Screen as ScreenService


class Coord(Vector2):
    class CoordType(Enum):
        NORMALIZED = 0
        ABSOLUTE = 1
        WORLD = 2
        RELATIVE = 3

    __slots__ = (
        "_x",
        "_y",
        "_absolute_x",
        "_absolute_y",
        "_type",
    )

    _x: float
    _y: float
    _absolute_x: float
    _absolute_y: float
    _type: CoordType

    def __init__(self, x=0.0, y=0.0, type=CoordType.NORMALIZED):
        super().__init__(x, y)

        self._type = type
        self._set_using_normalized(x, y)

    def to_tuple(self) -> tuple[float, float]:
        return (self._absolute_x, self._absolute_y)

    def _set_using_normalized(self, new_x: float, new_y: float):
        self._x = new_x
        self._y = new_y

        match self._type:
            case self.CoordType.NORMALIZED:
                self._absolute_x, self._absolute_y = (
                    ScreenService.normalized_to_absolute_coords(new_x, new_y)
                )
            case self.CoordType.WORLD:
                self._absolute_x, self._absolute_y = (
                    ScreenService.world_to_absolute_coords(new_x, new_y)
                )
            case _:
                self._absolute_x = new_x
                self._absolute_y = new_y

    def _set_using_absolute(self, new_x: float, new_y: float):
        self._absolute_x = new_x
        self._absolute_y = new_y

        match self._type:
            case self.CoordType.NORMALIZED:
                self._x, self._y = ScreenService.absolute_to_normalized_coords(
                    new_x, new_y
                )
            case self.CoordType.WORLD:
                self._x, self._y = ScreenService.absolute_to_world_coords(new_x, new_y)
            case _:
                self._x = new_x
                self._y = new_y

    @property
    def absolute_x(self) -> float:
        return self._absolute_x

    @absolute_x.setter
    def absolute_x(self, value: float):
        self._set_using_absolute(value, self.absolute_y)

    @property
    def absolute_y(self) -> float:
        return self._absolute_y

    @absolute_y.setter
    def absolute_y(self, value: float):
        self._set_using_absolute(self.absolute_x, value)

    @property
    def type(self) -> CoordType:
        return self._type

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float):
        self._set_using_normalized(value, self._y)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float):
        self._set_using_normalized(self._x, value)
