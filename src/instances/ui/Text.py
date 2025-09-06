import pyglet

from src.instances.core.MeshInstance import MeshInstance


class Text(MeshInstance):
    font: str = ""

    def create_mesh(self):
        batch = super().get_batch_for_mesh_or_error()

        if batch is None:
            return

        self.mesh = pyglet.text.Label(
            x=self.actual_position.x,
            y=self.actual_position.y,
            font_size=self.size.x,
            color=self.color.to_tuple(),
            batch=batch,
        )
