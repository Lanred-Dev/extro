import pyray
import os


class Font:
    __slots__ = ("_font",)

    _font: pyray.Font

    def __init__(self, font_path: str):
        self._font = pyray.load_font_ex(os.path.abspath(font_path), 96, None, 0)
        pyray.set_texture_filter(
            self._font.texture, pyray.TextureFilter.TEXTURE_FILTER_BILINEAR
        )

    def delete(self):
        pyray.unload_font(self._font)


__all__ = ["Font"]
