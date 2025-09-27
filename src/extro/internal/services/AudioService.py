"""Cache for sounds, to avoid loading the same sound multiple times. It does not handle music streams."""

import pyray

from extro.internal.utils.FileCache import FileCache

sound_cache = FileCache[pyray.Wave, pyray.Sound](
    pyray.load_wave, pyray.unload_wave, pyray.load_sound_from_wave
)
