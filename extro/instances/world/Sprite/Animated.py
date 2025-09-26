import pyray

from extro.instances.world.Sprite import Sprite
from extro.shared.Vector2 import Vector2
import extro.internal.systems.Animation as AnimationSystem


class AnimatedSprite(Sprite):
    _frame_size: Vector2
    _current_frame: int
    _frame_duration: float
    _last_frame_at: float
    _frame_count: int
    _is_active: bool

    def __init__(
        self,
        frame_size: Vector2 = Vector2(0, 0),
        frame_duration: float = 0.1,
        starting_frame: int = 0,
        is_active: bool = True,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
            source_size=frame_size,
        )

        self._is_active = is_active
        self._frame_count = int(self._texture.width // frame_size.x)
        self._frame_duration = frame_duration
        self._current_frame = starting_frame
        self._last_frame_at = pyray.get_time()
        self._frame_size = frame_size
        self._texture_source.x = self._current_frame * frame_size.x
        AnimationSystem.register_sprite(self._id)
        self._janitor.add(AnimationSystem.unregister_sprite, self._id)

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        self._is_active = is_active

    @property
    def frame(self) -> int:
        return self._current_frame
