import pyray

from extro.instances.core.Instance.Renderable import Renderable
from extro.shared.Vector2 import Vector2
import extro.Console as Console
import extro.internal.services.FileCache as FileCacheService


class Sprite(Renderable):
    __slots__ = Renderable.__slots__ + (
        "_image_file",
        "_texture",
        "_texture_source",
        "_source_position",
        "_use_texture_for_source_size",
    )

    _image_file: str
    _texture: pyray.Texture
    _texture_source: pyray.Rectangle
    _source_position: Vector2
    _use_texture_for_source_size: bool

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
        self._texture_source = pyray.Rectangle(
            source_position.x,
            source_position.y,
            (source_size.x if source_size else 0),
            (source_size.y if source_size else 0),
        )

        self._load_texture()
        self._janitor.add(self._unload_texture)

    def draw(self):
        pyray.draw_texture_pro(
            self._texture,
            self._texture_source,
            (*self.transform._actual_position, *self.transform._actual_size),
            self.transform._position_offset,
            self.transform._rotation,
            self.drawable.color.to_tuple(),
        )

    def _unload_texture(self):
        if getattr(self, "texture", None) is None:
            return

        FileCacheService.texture_cache.unload(self._image_file)

    def _load_texture(self):
        self._unload_texture()

        self._texture = FileCacheService.texture_cache.load(self._image_file)
        pyray.set_texture_filter(
            self._texture, pyray.TextureFilter.TEXTURE_FILTER_POINT
        )
        pyray.set_texture_wrap(self._texture, pyray.TextureWrap.TEXTURE_WRAP_CLAMP)

        if self._use_texture_for_source_size:
            self._texture_source.width = self._texture.width
            self._texture_source.height = self._texture.height

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

    @property
    def source_position(self) -> Vector2:
        return self._source_position

    @source_position.setter
    def source_position(self, position: Vector2):
        self._source_position = position.copy()
        self._texture_source.x = self._source_position.x
        self._texture_source.y = self._source_position.y

    @property
    def source_size(self) -> Vector2:
        return self._source_size.copy()

    @source_size.setter
    def source_size(self, size: Vector2 | None):
        if size is None:
            self._use_texture_for_source_size = True
            self._source_size = Vector2(self._texture.width, self._texture.height)
        else:
            self._use_texture_for_source_size = False
            self._source_size = size.copy()

        self._texture_source.width = self._source_size.x
        self._texture_source.height = self._source_size.y
