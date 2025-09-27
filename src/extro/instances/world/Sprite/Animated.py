import pyray

from extro.instances.world.Sprite import Sprite
from extro.shared.Vector2 import Vector2
import extro.internal.systems.Animation as AnimationSystem


class AnimatedSprite(Sprite):
    _frame_size: Vector2
    _current_frame: Vector2
    _frame_duration: float
    _last_frame_at: float
    _frame_count: int
    _is_active: bool

    def __init__(
        self,
        frame_size: Vector2,
        frame_duration: float = 0.1,
        is_active: bool = True,
        frame_count: int = 0,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
            source_size=frame_size,
        )

        self._is_active = is_active
        self._frame_count = frame_count
        self._frame_duration = frame_duration
        self._current_frame = Vector2(0, 0)
        # Force frame update on first update call
        self._last_frame_at = pyray.get_time() - frame_duration
        self._frame_size = frame_size

        AnimationSystem.register_sprite(self._id)
        self._janitor.add(AnimationSystem.unregister_sprite, self._id)

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        self._is_active = is_active

    @property
    def frame(self) -> Vector2:
        return self._current_frame
