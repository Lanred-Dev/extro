from extro.core.Instance import Instance
from extro.shared.types import InstanceUpdateType
from extro.core.Camera import Camera
import extro.Window as Window


class TargetCamera(Camera):
    _target: Instance | None

    def bind_to(self, target: "Instance | None", offset: tuple[float, float] = (0, 0)):
        """Bind the camera to an instance. The camera will follow the instance's position and rotation."""
        self._disconnect_target_connections()

        if target is None:
            self._target = None
            return

        self._camera.offset.x = Window.size.x / 2 + offset[0]
        self._camera.offset.y = Window.size.y / 2 + offset[1]

        self._target = target
        self._position = target.position.vector
        self._rotation = target.rotation
        self._target_connections["on_update"] = target.on_update.connect(
            self._handle_target_update
        )

    def _handle_target_update(self, property: InstanceUpdateType):
        if self._target is None:
            return

        match property:
            case InstanceUpdateType.POSITION:
                self._position = self._target._actual_position
                self._recalculate_position()
            case InstanceUpdateType.ROTATION:
                self._rotation = self._target.rotation

    def _disconnect_target_connections(self):
        if self._target is None or len(self._target_connections) == 0:
            return

        for signal, connection_id in self._target_connections.items():
            getattr(self._target, signal).disconnect(connection_id)

        self._target_connections.clear()
