from abc import abstractmethod
import pyray

from src.instances.core.DrawableInstance import DrawableInstance


class BackgroundInstance(DrawableInstance):
    __slots__ = ("_texture", "_texture_rect", "_texture_source")

    _texture: pyray.RenderTexture
    _texture_rect: pyray.Rectangle
    _texture_source: pyray.Rectangle

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._texture = pyray.load_render_texture(int(self._size.x), int(self._size.y))
        self._texture_rect = pyray.Rectangle(
            self._actual_position.x, self._actual_position.y, self._size.x, self._size.y
        )
        self._texture_source = pyray.Rectangle(0, 0, self._size.x, self._size.y)
        self._recalculate_texture()

    def destroy(self):
        super().destroy()
        pyray.unload_render_texture(self._texture)

    def draw(self):
        pyray.draw_texture_pro(
            self._texture.texture,
            self._texture_source,
            self._texture_rect,
            (0, 0),
            self._rotation,
            self._color.to_tuple(),
        )

    def _recalculate_texture(self):
        pyray.begin_texture_mode(self._texture)
        pyray.clear_background(pyray.BLANK)
        self._render_texture()
        pyray.end_texture_mode()

    def _apply_color(self):
        super()._apply_color()
        self._recalculate_texture()

    def _apply_size(self):
        self._texture_rect.width = self._size.x
        self._texture_rect.height = self._size.y
        self._texture_source.width = self._size.x
        self._texture_source.height = self._size.y
        self._recalculate_texture()

        super()._apply_size()

    def _apply_position(self):
        self._texture_rect.x = self._actual_position.x
        self._texture_rect.y = self._actual_position.y
        self._recalculate_texture()

        super()._apply_position()

    def _apply_rotation(self):
        self._recalculate_texture()
        super()._apply_rotation()

    @abstractmethod
    def _render_texture(self):
        raise NotImplementedError("Draw texture method must be implemented by subclass")
