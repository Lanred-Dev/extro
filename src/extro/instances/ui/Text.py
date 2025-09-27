import pyray

from extro.core.Instance.UI import UIInstance
from extro.instances.ui.Font import Font
from extro.assets.Fonts import Arial
from extro.shared.Coord import Coord, CoordType
import extro.Console as Console


class Text(UIInstance):
    __slots__ = UIInstance.__slots__ + (
        "_text",
        "_font",
        "_font_size",
        "_character_spacing",
    )

    _text: str
    _font: Font
    _character_spacing: int
    _font_size: int

    def __init__(
        self,
        text: str,
        font_size: int,
        font: Font = Arial,
        character_spacing: int = 1,
        **kwargs,
    ):
        # Dont allow size to be set, as it is determined by the font size
        if "size" in kwargs:
            del kwargs["size"]

        super().__init__(**kwargs)

        self._text = text
        self._font = font
        self._character_spacing = character_spacing
        self._font_size = font_size

        self._invalidation_manager.invalidate(self._scale_size_to_fix_text, 3)

    def draw(self):
        pyray.draw_text_pro(
            self._font._font,
            self._text,
            self._actual_position.to_tuple(),
            self._render_origin.to_tuple(),
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
        self._font_size = int(size * (self._scale.x + self._scale.y))
        self._invalidation_manager.invalidate(self._scale_size_to_fix_text, 3)

    @UIInstance.size.setter
    def size(self, *_: object, **__: object):
        Console.log("Cannot set size of `Text` instance", Console.LogType.WARNING)

    def _scale_size_to_fix_text(self):
        text_size: pyray.Vector2 = pyray.measure_text_ex(
            self._font._font, self._text, self._font_size, self._character_spacing
        )
        self._size = Coord(text_size.x, text_size.y, CoordType.ABSOLUTE)
        self._recalculate_size()
