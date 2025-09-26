from enum import Enum

from extro.shared.Vector2 import Vector2
import extro.services.Screen as ScreenService


class CoordType(Enum):
    NORMALIZED = 0
    ABSOLUTE = 1
    WORLD = 2
    PARENT = 3


class Coord:
    type: CoordType
    _vector: Vector2
    _is_dirty: bool
    _x: float
    _y: float

    def __init__(self, x: float, y: float, type: CoordType):
        self.type = type
        self._x = x
        self._y = y
        self._is_dirty = True

    def __repr__(self):
        return f"Coord({self._x}, {self._y}, {self.type})"

    def _recompute_vector_if_dirty(self):
        if not self._is_dirty:
            return

        match self.type:
            case CoordType.NORMALIZED:
                self._vector = ScreenService.normalized_to_screen_coords(
                    Vector2(self._x, self._y)
                )
            case CoordType.WORLD:
                self._vector = ScreenService.world_to_screen_coords(
                    Vector2(self._x, self._y)
                )
            case _:
                self._vector = Vector2(self._x, self._y)

        self._is_dirty = False

    @property
    def x(self) -> float:
        self._recompute_vector_if_dirty()
        return self._x

    @x.setter
    def x(self, x: float):
        self._x = x
        self._is_dirty = True

    @property
    def y(self) -> float:
        self._recompute_vector_if_dirty()
        return self._y

    @y.setter
    def y(self, y: float):
        self._y = y
        self._is_dirty = True

    @property
    def vector(self) -> Vector2:
        self._recompute_vector_if_dirty()
        return self._vector
