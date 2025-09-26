import pyray

from extro.core.Instance.Drawable import DrawableInstance
from extro.shared.Vector2 import Vector2
import extro.Console as Console
import extro.internal.services.ImageService as ImageService


class Sprite(DrawableInstance):
    _image_file: str
    _texture: pyray.Texture
    _texture_rect: pyray.Rectangle
    _texture_source: pyray.Rectangle
    _source_size: Vector2 | None
    _source_position: Vector2

    def __init__(
        self,
        image_file: str,
        source_size: Vector2 | None = None,
        source_position: Vector2 = Vector2(0, 0),
        **kwargs,
    ):
        super().__init__(**kwargs)

        if source_size is None:
            source_size = Vector2(self._texture.width, self._texture.height)
            self._source_size = None
        else:
            self._source_size = source_size

        self._image_file = image_file
        self._source_position = source_position

        self._load_texture()
        self._texture_rect = pyray.Rectangle(
            self._actual_position.x,
            self._actual_position.y,
            self._actual_size.x,
            self._actual_size.y,
        )
        self._texture_source = pyray.Rectangle(
            source_position.x,
            source_position.y,
            source_size.x,
            source_size.y,
        )

        self._janitor.add(self._unload_texture)

    def draw(self):
        pyray.draw_texture_pro(
            self._texture,
            self._texture_source,
            self._texture_rect,
            self._render_origin.to_tuple(),
            self._rotation,
            self._color.to_tuple(),
        )

    def _apply_size(self):
        self._texture_rect.width = self._actual_size.x
        self._texture_rect.height = self._actual_size.y
        super()._apply_size()

    def _apply_position(self):
        self._texture_rect.x = self._actual_position.x
        self._texture_rect.y = self._actual_position.y
        super()._apply_position()

    def _unload_texture(self):
        ImageService.texture_cache.unload_if_needed(self._image_file)

    def _load_texture(self):
        self._texture = ImageService.texture_cache.get(self._image_file)

    @property
    def image(self) -> str:
        return self._image_file

    @image.setter
    def image(self, image: str):
        self._image_file = image
        self._unload_texture()
        self._load_texture()

        source_size = (
            self._source_size
            if self._source_size
            else Vector2(self._texture.width, self._texture.height)
        )
        self._texture_source.width = source_size.x
        self._texture_source.height = source_size.y

        Console.log(f"{self.id} image was changed to {image}", Console.LogType.DEBUG)
