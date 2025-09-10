from typing import List

from src.instances.core.Instance import Instance
from src.instances.core.CollisionMask import CollisionMask
from src.internal.components.Signal import Signal
import src.internal.CollisionHandler as CollisionHandler


class CollisionInstance(Instance):
    __slots__ = (
        "_is_collidable",
        "_collision_group",
        "_collision_mask",
        "_colliding_width",
        "on_collision",
        "on_collision_end",
    )

    _is_collidable: bool
    _collision_group: str
    _collision_mask: CollisionMask
    _colliding_width: List[str]

    on_collision: Signal
    on_collision_end: Signal

    def __init__(self, is_collidable: bool = True, collision_group="", **kwargs):
        super().__init__(**kwargs)

        self._is_collidable = is_collidable
        self._collision_group = collision_group
        self._collision_mask = CollisionMask(
            position=self._actual_position,
            size=self._actual_size,
            rotation=self._rotation,
        )

        self.on_collision = Signal()
        self.on_collision_end = Signal()

        self._janitor.add(self.on_collision)
        self._janitor.add(self.on_collision_end)
        self._janitor.add(CollisionHandler.unregister_instance, self.id)

        CollisionHandler.register_instance(self.id)

    @property
    def is_collidable(self) -> bool:
        return self._is_collidable

    @is_collidable.setter
    def is_collidable(self, is_collidable: bool):
        self._is_collidable = is_collidable
        CollisionHandler._recompute_collidable_instances()

    @property
    def collision_group(self) -> str:
        return self._collision_group

    @collision_group.setter
    def collision_group(self, collision_group: str):
        self._collision_group = collision_group
        CollisionHandler._recompute_collidable_instances()

    def _apply_size(self):
        super()._apply_size()
        self._collision_mask.size = self._actual_size

    def _apply_position(self):
        super()._apply_position()
        self._collision_mask.position = self._actual_position

    def _apply_rotation(self):
        super()._apply_rotation()
        self._collision_mask.rotation = self._rotation
