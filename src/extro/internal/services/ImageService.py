import pyray

from extro.internal.utils.FileCache import FileCache

texture_cache = FileCache[pyray.Texture, pyray.Texture](
    pyray.load_texture, pyray.unload_texture
)
