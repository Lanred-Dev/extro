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
    for instance_id in tweens.instances[:]:
        instance: "Tween" = InstanceManager.instances[instance_id]  # type: ignore

        if not instance._is_active:
            continue

        instance.elapsed += TimingService.delta
        instance.progress = instance.easing(
            min(instance.elapsed / instance.duration, 1)
        )
        instance.value = lerp(instance.start, instance.end, instance.progress)
        instance.on_update.fire(instance.value)

        if instance.elapsed >= instance.duration:
            instance._is_active = False
            instance.progress = 1.0
            instance.value = instance.end
            instance.on_finish.fire()

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
