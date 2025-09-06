from typing import List

from src.instances.core.MeshInstance import MeshInstance
from src.values.Vector2 import Vector2
from src.instances.core.CollisionMask import CollisionMask
from src.internal.components.Signal import Signal
from src.internal.CollisionHandler import CollisionHandler


class CollisionInstance(MeshInstance):
    is_collidable: bool
    collision_group: str = ""
    collision_mask: CollisionMask
    colliding_width: List[str]

    on_collision: Signal
    on_collision_end: Signal

    def __init__(self):
        super().__init__()
        self.is_collidable = True
        self.colliding_width = []
        self.on_collision = Signal()
        self.on_collision_end = Signal()
        self.janitor.add(self.on_collision)
        self.janitor.add(self.on_collision_end)
        CollisionHandler.register_instance(self.id)

    def destroy(self):
        super().destroy()
        CollisionHandler.unregister_instance(self.id)

    def create_mesh(self):
        super().create_mesh()
        self.__create_collision_mask()

    def __create_collision_mask(self):
        self.collision_mask = CollisionMask(
            position=self.actual_position,
            size=self.size,
            rotation=self.rotation,
        )

    def _apply_position(self):
        self.collision_mask.set_position(self.actual_position)

    def _apply_size(self):
        self.collision_mask.set_size(self.size)

    def _apply_rotation(self):
        self.collision_mask.set_rotation(self.rotation)
