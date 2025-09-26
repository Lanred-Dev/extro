import pyray

from extro.internal.utils.FileCache import FileCache

image_cache = FileCache[pyray.Image, pyray.Image](pyray.load_image, pyray.unload_image)
texture_cache = FileCache[pyray.Texture, pyray.Texture](
    pyray.load_texture, pyray.unload_texture
)
