import pyglet

from src.instances.core.CollisionInstance import CollisionInstance


class Sprite(CollisionInstance):
    image: pyglet.image.AbstractImage

    def set_image(self, path: str):
        self.image = pyglet.image.load(path)
        self.mark_dirty(self._apply_image)

    def create_mesh(self):
        batch = super().get_batch_for_mesh_or_error()

        if batch is None:
            return

        self.mesh = pyglet.sprite.Sprite(
            img=self.image,
            x=self.actual_position.x,
            y=self.actual_position.y,
            batch=batch,
        )
        super().create_mesh()
        self.mesh.scale_x = self.size.x / self.image.width
        self.mesh.scale_y = self.size.y / self.image.height
        self.mesh.rotation = self.rotation

    def _apply_position(self):
        super()._apply_position()
        self.mesh.position = (self.actual_position.x, self.actual_position.y, 0)

    def _apply_size(self):
        super()._apply_size()
        self.mesh.scale_x = self.size.x / self.image.width
        self.mesh.scale_y = self.size.y / self.image.height

    def _apply_color(self):
        self.mesh.color = self.color.to_tuple()

    def _apply_rotation(self):
        super()._apply_rotation()
        self.mesh.rotation = self.rotation

    def _apply_image(self):
        self.mesh.img = self.image
