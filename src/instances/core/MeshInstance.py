from abc import abstractmethod
from typing import Any

from src.instances.core.Instance import Instance


class MeshInstance(Instance):
    __slots__ = ("_mesh",)

    _mesh: Any

    def _apply_new_batch(self):
        super()._apply_new_batch()
        self.create_mesh()

    def _recalculate_position(self):
        self._position_offset = self._actual_size / 2
        super()._recalculate_position()

    def _recalculate_size(self):
        super()._recalculate_size()
        self._center_mesh_anchor()

    @abstractmethod
    def create_mesh(self):
        pass

    def _create_mesh(self, component: Any, **kwargs: Any):
        if self._scene is None:
            return

        self._mesh = component(**kwargs, batch=self._scene._batch)
        self._center_mesh_anchor()

    def _center_mesh_anchor(self):
        self._mesh.anchor_x = self._actual_size.x / 2
        self._mesh.anchor_y = self._actual_size.y / 2
