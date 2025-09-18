import pyray

from src.instances.core.Instance import Instance, InstanceUpdateType
import src.internal.services.WorldService as WorldService


class Camera:
    _camera: pyray.Camera2D
    _target: Instance | None
    _target_connections: dict[str, str]

    def __init__(self, target: Instance | None = None, zoom: float = 1.0):
        self._camera = pyray.Camera2D()
        self._target = None
        self.bind_to(target)

    def bind_to(self, target: "Instance | None"):
        self._disconnect_target_connections()

        if target is None:
            self._target = None
            return

        self._target = target
        self._camera.target.x = target.position.x
        self._camera.target.y = target.position.y
        self._camera.rotation = target.rotation
        self._target_connections["on_update"] = target.on_update.connect(
            self._handle_target_update
        )

    def make_active(self):
        WorldService._set_camera(self._camera)

    def _handle_target_update(self, property: InstanceUpdateType):
        # If this is called, we know that _target is not None
        match property:
            case InstanceUpdateType.POSITION:
                self._camera.target.x = self._target.position.x  # type: ignore
                self._camera.target.y = self._target.position.y  # type: ignore
            case InstanceUpdateType.ROTATION:
                self._camera.rotation = self._target.rotation  # type: ignore

    def _disconnect_target_connections(self):
        if self._target is None:
            return

        for signal, connection_id in self._target_connections.items():
            getattr(self._target, signal).disconnect(connection_id)

        self._target_connections.clear()

    @property
    def zoom(self):
        return self._camera.zoom

    @zoom.setter
    def zoom(self, zoom: float):
        self._camera.zoom = zoom
