from typing import TYPE_CHECKING

from src.instances.core.Instance import Instance
from src.internal.shared_types import RenderTargetType

if TYPE_CHECKING:
    from src.internal.helpers.Signal import Signal


class ProximityArea(Instance):
    on_enter: "Signal"
    on_exit: "Signal"

    def __init__(self, collision_group: str = "", **kwargs):
        super().__init__(**kwargs)

        self.add_collider(collision_group=collision_group)
        self.on_enter = self.collider.on_collision
        self.on_exit = self.collider.on_collision_end

    def _recalculate_position(self, *_: object, **__: object):
        super()._recalculate_position(self._actual_size / 2, RenderTargetType.WORLD)

    @property
    def collision_group(self) -> str:
        return self.collider._collision_group

    @collision_group.setter
    def collision_group(self, group: str):
        self.collider._collision_group = group
