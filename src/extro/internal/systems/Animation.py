from typing import TYPE_CHECKING
import pyray
from enum import Enum, auto

import extro.internal.InstanceManager as InstanceManager
from extro.internal.utils.InstanceRegistry import InstanceRegistry
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    from extro.animation.Tween import Tween


class AnimatedInstanceType(Enum):
    ANIMATOR = auto()
    TWEEN = auto()


tweens: InstanceRegistry = InstanceRegistry(
    "Animation System",
)


def update():
    now: float = pyray.get_time()

    for animator in ComponentManager.animators.values():
        if (
            not animator._is_active
            or now - animator._last_frame_at < animator._frame_duration
        ):
            continue

        animator._current_frame.x = (
            animator._current_frame.x + 1
        ) % animator._frame_count
        animator._texture_source.x = (
            animator._current_frame.x * animator._texture_source.width
        )
        animator._texture_source.y = (
            animator._current_frame.y * animator._texture_source.height
        )
        animator._last_frame_at = now
