import pyray

from extro.instances.world.Sprite import Sprite
from extro.shared.Vector2C import Vector2
from extro.instances.core.components.Animator import Animator


class AnimatedSprite(Sprite):
    __slots__ = Sprite.__slots__ + ("animator",)

    animator: "Animator"

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

        animator: Animator = Animator(
            self._id,
            texture_source=self._texture_source,
            frame_duration=frame_duration,
            is_active=is_active,
            frame_count=frame_count,
        )
        self.add_component(animator)
        self.animator = animator
