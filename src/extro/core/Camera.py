import pyray

from extro.core.Instance import Instance
from extro.shared.Vector2 import Vector2


class Camera:
    __slots__ = (
        "_camera",
        "_position",
        "_rotation",
    )

    _camera: pyray.Camera2D
    _position: Vector2
    _rotation: float

    def __init__(
        self,
        position: Vector2 = Vector2(0, 0),
        rotation: float = 0.0,
        zoom: float = 1.0,
    ):
        self._camera = pyray.Camera2D()
        self._camera.zoom = zoom
        self._position = position
        self._rotation = rotation
        self._recalculate_position()

    def _recalculate_position(self):
        self._camera.target.x = self._position.x
        self._camera.target.y = self._position.y

    def _recalculate_rotation(self):
        self._camera.rotation = self._rotation

    @property
    def zoom(self) -> float:
        return self._camera.zoom

    @zoom.setter
    def zoom(self, zoom: float):
        self._camera.zoom = zoom

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, position: Vector2):
        self._position = position
        self._recalculate_position()
