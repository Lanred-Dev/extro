import pyray

from extro.shared.Vector2C import Vector2


class Camera:
    __slots__ = (
        "_camera",
        "_position",
    )

    _camera: pyray.Camera2D
    _position: Vector2

    def __init__(
        self,
        position: Vector2 = Vector2(0, 0),
        rotation: float = 0.0,
        zoom: float = 1.0,
    ):
        self._camera = pyray.Camera2D()
        self.zoom = zoom
        self.rotation = rotation
        self.position = position

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
    def rotation(self) -> float:
        return self._camera.rotation

    @rotation.setter
    def rotation(self, rotation: float):
        self._camera.rotation = rotation

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, position: Vector2):
        self._position = position
        self._recalculate_position()
