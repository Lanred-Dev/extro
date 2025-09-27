from typing import TYPE_CHECKING

from extro.shared.types import InstanceUpdateType
from extro.core.Camera import Camera
import extro.Window as Window

if TYPE_CHECKING:
    from extro.core.Instance import Instance
    from extro.shared.Vector2 import Vector2


class TargetCamera(Camera):
    __slots__ = Camera.__slots__ + (
        "_offset",
        "_target",
        "_target_connections",
        "_window_resize_connection",
    )

    _target: "Instance | None"
    _target_connections: dict[str, str]
    _window_resize_connection: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._target = None
        self._target_connections = {}

        self._window_resize_connection = Window.on_resize.connect(
            self._handle_window_resize
        )
        self._handle_window_resize(Window.size)

    def destroy(self):
        """Destroy the camera and unbind it from its target."""
        self._disconnect_target_connections()
        Window.on_resize.disconnect(self._window_resize_connection)

    def bind_to(self, target: "Instance | None"):
        """Bind the camera to an instance. The camera will follow the instance's position and rotation."""
        self._disconnect_target_connections()

        if target is None:
            self._target = None
            return

        self._target = target
        self._position = target.position.vector
        self._rotation = target.rotation
        self._target_connections["on_update"] = target.on_update.connect(
            self._handle_target_update
        )

    def _handle_window_resize(self, new_size: "Vector2"):
        self._camera.offset.x = new_size.x / 2
        self._camera.offset.y = new_size.y / 2

    def _handle_target_update(self, property: InstanceUpdateType):
        if self._target is None:
            return

        match property:
            case InstanceUpdateType.POSITION:
                self._position = self._target._actual_position
                self._recalculate_position()
            case InstanceUpdateType.ROTATION:
                self._rotation = self._target.rotation
                self._recalculate_rotation()

    def _disconnect_target_connections(self):
        if self._target is None or len(self._target_connections) == 0:
            return

        for signal, connection_id in self._target_connections.items():
            getattr(self._target, signal).disconnect(connection_id)

        self._target_connections.clear()
