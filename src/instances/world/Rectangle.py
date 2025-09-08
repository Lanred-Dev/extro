import pyglet

from src.instances.core.CollisionInstance import CollisionInstance


class Rectangle(CollisionInstance):
    def create_mesh(self):
        self._create_mesh(
            pyglet.shapes.Rectangle,
            x=self._actual_position.x,
            y=self._actual_position.y,
            width=self._size.x,
            height=self._size.y,
            color=self._color.to_tuple(),
        )
        self._mesh.rotation = self._rotation

    def _apply_position(self):
        super()._apply_position()
        self._mesh.position = self._actual_position.to_tuple()

    def _apply_size(self):
        super()._apply_size()
        self._mesh.width = self._size.x
        self._mesh.height = self._size.y

    def _apply_color(self):
        super()._apply_color()
        self._mesh.color = self._color.to_tuple()

    def _apply_rotation(self):
        super()._apply_rotation()
        self._mesh.rotation = self._rotation
