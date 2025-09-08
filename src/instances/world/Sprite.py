import pyglet

from src.instances.core.CollisionInstance import CollisionInstance


class Sprite(CollisionInstance):
    __slots__ = ("_image",)

    _image: pyglet.image.AbstractImage

    def __init__(self, image: str, **kwargs):
        self._image = pyglet.image.load(image)
        super().__init__(**kwargs)

    def create_mesh(self):
        self._create_mesh(
            pyglet.sprite.Sprite,
            x=self._actual_position.x,
            y=self._actual_position.y,
            img=self._image,
        )
        self._mesh.color = self._color.to_tuple()
        self._mesh.rotation = self._rotation
        self._mesh.scale_x = self._actual_size.x / self._image.width
        self._mesh.scale_y = self._actual_size.y / self._image.height

    @property
    def image(self) -> pyglet.image.AbstractImage:
        return self._image

    @image.setter
    def image(self, image: str):
        self._image = pyglet.image.load(image)
        self.invalidate(self._apply_image)

    def _apply_image(self):
        self._mesh.image = self._image

    def _apply_position(self):
        super()._apply_position()
        self._mesh.position = (self._actual_position.x, self._actual_position.y, 0)

    def _apply_size(self):
        super()._apply_size()
        self._mesh.scale_x = self._actual_size.x / self._image.width
        self._mesh.scale_y = self._actual_size.y / self._image.height

    def _apply_color(self):
        super()._apply_color()
        self._mesh.color = self._color.to_tuple()

    def _apply_rotation(self):
        super()._apply_rotation()
        self._mesh.rotation = self._rotation
