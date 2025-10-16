from typing import TYPE_CHECKING
from enum import Enum, auto
import pyray

import extro.internal.InstanceManager as InstanceManager
from extro.internal.utils.InstanceRegistry import InstanceRegistry
import extro.internal.ComponentManager as ComponentManager
import extro.services.Timing as TimingService
from extro.animation.lerp import lerp

if TYPE_CHECKING:
    from extro.animation.Tween import Tween


class AnimatedInstanceType(Enum):
    ANIMATOR = auto()
    TWEEN = auto()


tweens: InstanceRegistry = InstanceRegistry(
    "Animation System",
)


def update():
    for tween_id in tweens.instances[:]:
        tween: "Tween" = InstanceManager.instances[tween_id]  # type: ignore

        if not tween.is_playing:
            continue

        tween._elapsed += TimingService.delta
        tween.progress = tween.easing(min(tween._elapsed / tween.duration, 1))
        tween.value = lerp(tween.start, tween.end, tween.progress)
        tween.on_update.fire()

        if tween._elapsed >= tween.duration:
            tween._is_playing = False
            tween.progress = 1.0
            tween.value = tween.end
            tween.on_finish.fire()

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
