from typing import Any
import pyglet
from abc import ABCMeta, abstractmethod

from src.values.Color import Color
from src.instances.core.Instance import Instance
from src.values.Vector2 import Vector2
from src.internal.Console import Console, LogType


class MeshInstance(Instance, metaclass=ABCMeta):
    mesh: Any
    rotation: int

    def __init__(self):
        super().__init__()
        self.rotation = 0

    def set_color(self, color: Color):
        super().set_color(color)
        self.mark_dirty(self._apply_color)

    def set_size(self, size: Vector2):
        super().set_size(size)
        self.mark_dirty(self._apply_size)
        self.mark_dirty(self._apply_mesh_anchor)

    def set_position(self, position: Vector2):
        super().set_position(position)
        self.mark_dirty(self._apply_position)

    def set_rotation(self, rotation: int):
        self.rotation = rotation
        self.mark_dirty(self._apply_rotation)

    def _apply_anchor_to_position(self):
        super()._apply_anchor_to_position()
        # All instances are calculated from their center when rendered from pyglet, so move them back
        self.actual_position.x += self.size.x / 2
        self.actual_position.y += self.size.y / 2

    def _on_parent_update(self):
        super()._on_parent_update()
        self._apply_position()

    @abstractmethod
    def create_mesh(self):
        self._apply_mesh_anchor()
        self._apply_anchor_to_position()

    def get_batch_for_mesh_or_error(self) -> pyglet.graphics.Batch | None:
        if self.scene is None:
            Console.log(
                "Cannot call `get_batch_for_mesh_or_error` if instance is not apart of a scene.",
                LogType.ERROR,
            )
            return None

        return self.scene.batch

    @abstractmethod
    def _apply_color(self):
        pass

    @abstractmethod
    def _apply_size(self):
        pass

    @abstractmethod
    def _apply_position(self):
        pass

    @abstractmethod
    def _apply_rotation(self):
        pass

    def _apply_mesh_anchor(self):
        self.mesh.anchor_x = self.size.x / 2
        self.mesh.anchor_y = self.size.y / 2
