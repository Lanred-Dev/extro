import pyglet

from src.instances.core.CollisionInstance import CollisionInstance


class Rectangle(CollisionInstance):
    def create_mesh(self):
        batch = super().get_batch_for_mesh_or_error()

        if batch is None:
            return

        self.mesh = pyglet.shapes.Rectangle(
            x=self.actual_position.x,
            y=self.actual_position.y,
            width=self.size.x,
            height=self.size.y,
            color=self.color.to_tuple(),
            batch=batch,
        )
        self.mesh.rotation = self.rotation
        super().create_mesh()

    def _apply_position(self):
        super()._apply_position()
        self.mesh.position = self.actual_position.to_tuple()

    def _apply_size(self):
        super()._apply_size()
        self.mesh.width = self.size.x
        self.mesh.height = self.size.y

    def _apply_color(self):
        self.mesh.color = self.color.to_tuple()

    def _apply_rotation(self):
        super()._apply_rotation()
        self.mesh.rotation = self.rotation
