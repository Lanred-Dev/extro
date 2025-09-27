from typing import TYPE_CHECKING

from extro.core.Instance import Instance
import extro.Console as Console

if TYPE_CHECKING:
    from extro.utils.Signal import Signal


class ProximityArea(Instance):
    __slots__ = Instance.__slots__ + (
        "on_enter",
        "on_exit",
    )

    on_enter: "Signal"
    on_exit: "Signal"

    def __init__(self, collision_group: str = "", **kwargs):
        super().__init__(**kwargs)

        self.add_collider(collision_group=collision_group)
        self.on_enter = self.collider.on_collision
        self.on_exit = self.collider.on_collision_end

    def _recalculate_position(self, *_: object, **__: object):
        super()._recalculate_position(self._actual_size / 2)

    def add_physics_body(self, mass: float = 1.0, is_anchored: bool = False):
        Console.log("ProximityArea cannot have a physics body", Console.LogType.WARNING)

    def add_child(self, child: Instance):
        Console.log("ProximityArea cannot have children", Console.LogType.WARNING)

    @property
    def collision_group(self) -> str:
        return self.collider._collision_group

    @collision_group.setter
    def collision_group(self, group: str):
        self.collider._collision_group = group
