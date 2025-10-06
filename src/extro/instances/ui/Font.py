import pyray
import os


class Font:
    __slots__ = ("_instance",)

    _instance: pyray.Font

    def __init__(self, font_path: str):
        self._instance = pyray.load_font_ex(os.path.abspath(font_path), 96, None, 0)
        pyray.set_texture_filter(
            self._instance.texture, pyray.TextureFilter.TEXTURE_FILTER_BILINEAR
        )

    def delete(self):
        pyray.unload_font(self._instance)

    def __call__(self):
        return self._instance

    def __repr__(self) -> str:
        return f"Font({self._instance})"


__all__ = ["Font"]
