import pyray

from src.instances.core.Instance import Instance
from src.instances.ui.Font import Font
from src.values.Vector2 import Vector2


class Text(Instance):
    __slots__ = ("_text", "_font", "_font_size", "_character_spacing")

    _text: str
    _font: Font
    _character_spacing: int
    _font_size: int

    def __init__(
        self,
        text: str,
        font: Font,
        font_size: int,
        character_spacing: int = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._text = text
        self._font = font
        self._character_spacing = character_spacing
        self._font_size = font_size
        self.invalidate(self._scale_size_to_fix_text)

    def draw(self):
        pyray.draw_text_pro(
            self._font._font,
            self._text,
            (self._actual_position.x, self._actual_position.y),
            (0, 0),
            self._rotation,
            self._font_size,
            self._character_spacing,
            self._color.to_tuple(),
        )

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    @property
    def character_spacing(self):
        return self._character_spacing

    @character_spacing.setter
    def character_spacing(self, spacing: int):
        self._character_spacing = spacing

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size: int):
        self._font_size = size
        self.invalidate(self._scale_size_to_fix_text)

    @Instance.size.setter
    def size(self, size: Vector2):
        text_length: pyray.Vector2 = pyray.measure_text_ex(
            self._font._font, self._text, size.y, self._character_spacing
        )

        if size.x < text_length.x:
            size.y = (size.x / text_length.x) * size.y

        self._font_size = int(size.y)

        if size.x < 0 and size.y < 0:
            self._is_position_relative = True
            size.x = abs(size.x)
            size.y = abs(size.y)
        else:
            self._is_position_relative = False

        self._size = size
        self.invalidate(self._recalculate_size)

    def _scale_size_to_fix_text(self):
        text_length: pyray.Vector2 = pyray.measure_text_ex(
            self._font._font, self._text, self._font_size, self._character_spacing
        )
        self._actual_size = Vector2(text_length.x, text_length.y)
        self.invalidate(self._apply_size)
