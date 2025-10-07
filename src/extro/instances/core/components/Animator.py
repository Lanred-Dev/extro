from typing import TYPE_CHECKING
import pyray

from extro.instances.core.components.Component import Component
from extro.shared.Vector2C import Vector2
import extro.internal.ComponentManager as ComponentManager
import extro.internal.systems.Animation as AnimationSystem

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager


class Animator(Component):
    __slots__ = Component.__slots__ + (
        "_texture_source",
        "_current_frame",
        "_frame_duration",
        "_last_frame_at",
        "_frame_count",
        "_is_active",
        "_owner",
    )

    _key = "animator"

    _current_frame: Vector2
    _frame_duration: float
    _last_frame_at: float
    _frame_count: int
    _is_active: bool
    _owner: "InstanceManager.InstanceIDType"

    def __init__(
        self,
        owner: "InstanceManager.InstanceIDType",
        texture_source: pyray.Rectangle,
        frame_duration: float,
        is_active: bool,
        frame_count: int,
    ):
        super().__init__(owner, ComponentManager.ComponentType.ANIMATOR)

        self._is_active = is_active
        self._frame_count = frame_count
        self._frame_duration = frame_duration
        self._current_frame = Vector2(0, 0)
        # Force frame update on first update call
        self._last_frame_at = pyray.get_time() - frame_duration
        self._texture_source = texture_source

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        self._is_active = is_active

    @property
    def frame(self) -> Vector2:
        return self._current_frame
