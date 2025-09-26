import pyray

from extro.core.Instance import Instance
from extro.shared.Vector2 import Vector2


class Camera:
    _camera: pyray.Camera2D
    _target: Instance | None
    _target_connections: dict[str, str]
    _position: Vector2

    def __init__(self, position: Vector2 = Vector2(0, 0), zoom: float = 1.0):
        self._camera = pyray.Camera2D()
        self._camera.zoom = zoom
        self._target = None
        self._position = position
        self._target_connections = {}
        self._recalculate_position()

    def _recalculate_position(self):
        self._camera.target.x = self._position.x
        self._camera.target.y = self._position.y

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
