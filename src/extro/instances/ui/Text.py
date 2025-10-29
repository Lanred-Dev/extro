import pyray

from extro.instances.core.Instance.UI import UIInstance
from extro.instances.ui.Font import Font
from extro.assets.Fonts import Arial
import extro.internal.systems.UI as UISystem
from extro.shared.Coord import Coord


class Text(UIInstance):
    __slots__ = UIInstance.__slots__ + (
        "text",
        "font",
        "_font_size",
        "character_spacing",
        "scale_size_to_font",
        "_is_font_size_dirty",
    )

    text: str
    font: Font
    character_spacing: int
    _font_size: int
    scale_size_to_font: bool
    _is_font_size_dirty: bool

    def __init__(
        self,
        text: str,
        font_size: int,
        size: Coord = Coord(0, 0, Coord.CoordType.ABSOLUTE),
        font: Font = Arial,
        character_spacing: int = 1,
        scale_size_to_font: bool = False,
        **kwargs,
    ):
        super().__init__(type=UISystem.UIInstanceType.TEXT, size=size, **kwargs)

        self.text = text
        self.font = font
        self.character_spacing = character_spacing
        self._font_size = font_size
        self.scale_size_to_font = scale_size_to_font
        self._is_font_size_dirty = True

    def draw(self):
        pyray.draw_text_pro(
            self.font(),
            self.text,
            self.transform._actual_position,
            self.transform._position_offset,
            self.transform._rotation,
            self._font_size,
            self.character_spacing,
            self.drawable.color.to_tuple(),
        )

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, size: int):
        self._font_size = size
        self._is_font_size_dirty = True
