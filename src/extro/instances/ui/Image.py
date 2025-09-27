import pyray

from extro.core.Instance.UI import UIInstance
from extro.shared.Vector2 import Vector2
import extro.Console as Console
import extro.internal.services.ImageService as ImageService


class Image(UIInstance):
    __slots__ = UIInstance.__slots__ + (
        "_image_file",
        "_texture",
        "_texture_rect",
        "_texture_source",
        "_source_size",
        "_source_position",
        "_use_texture_for_source_size",
        "_texture_initialized",
    )

    _image_file: str
    _texture: pyray.Texture
    _texture_rect: pyray.Rectangle
    _texture_source: pyray.Rectangle
    _source_size: Vector2
    _source_position: Vector2
    _use_texture_for_source_size: bool
    _texture_initialized: bool

    def __init__(
        self,
        image_file: str,
        source_size: Vector2 | None = None,
        source_position: Vector2 = Vector2(0, 0),
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._image_file = image_file
        self._source_position = source_position.copy()
        self._use_texture_for_source_size = source_size is None
        self._source_size = source_size or Vector2(0, 0)
        self._texture_initialized = False

        self._texture_rect = pyray.Rectangle(
            self._actual_position.x,
            self._actual_position.y,
            self._actual_size.x,
            self._actual_size.y,
        )
        self._texture_source = pyray.Rectangle(
            self._source_position.x,
            self._source_position.y,
            self._source_size.x,
            self._source_size.y,
        )

        self._load_texture()
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
        if not self._texture_initialized:
            return

        ImageService.texture_cache.unload(self._image_file)

    def _load_texture(self):
        self._unload_texture()

        self._texture = ImageService.texture_cache.load(self._image_file)
        pyray.set_texture_filter(
            self._texture, pyray.TextureFilter.TEXTURE_FILTER_POINT
        )
        pyray.set_texture_wrap(self._texture, pyray.TextureWrap.TEXTURE_WRAP_CLAMP)

        if self._use_texture_for_source_size:
            self._source_size = Vector2(self._texture.width, self._texture.height)

        self._texture_source.width = self._source_size.x
        self._texture_source.height = self._source_size.y
        self._texture_initialized = True

    @property
    def image(self) -> str:
        return self._image_file

    @image.setter
    def image(self, image_file: str):
        self._image_file = image_file
        self._load_texture()
        Console.log(
            f"{self.id} image was changed to {image_file}", Console.LogType.DEBUG
        )
