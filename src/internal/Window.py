import pyray

from src.values.Vector2 import Vector2

_PRIMARY_MONITOR_INDEX: int = 0

title: str = "extro engine"
size: Vector2 = Vector2(500, 500)
fullscreen: bool = False

pyray.set_config_flags(pyray.ConfigFlags.FLAG_MSAA_4X_HINT)
pyray.set_config_flags(pyray.ConfigFlags.FLAG_WINDOW_HIGHDPI)
pyray.init_window(int(size.x), int(size.y), title)
pyray.set_window_state(pyray.ConfigFlags.FLAG_WINDOW_ALWAYS_RUN)


def set_title(title: str):
    pyray.set_window_title(title)


def set_size(new_size: Vector2):
    pyray.set_window_size(int(size.x), int(size.y))


def toggle_fullscreen():
    global fullscreen, size
    fullscreen = not fullscreen

    if not fullscreen:
        pyray.set_window_size(int(size.x), int(size.y))
    else:
        size = Vector2(
            pyray.get_monitor_width(_PRIMARY_MONITOR_INDEX),
            pyray.get_monitor_height(_PRIMARY_MONITOR_INDEX),
        )
        pyray.set_window_size(int(size.x), int(size.y))

    pyray.toggle_fullscreen()


def _close():
    pyray.close_window()


__all__ = [
    "set_title",
    "set_size",
    "fullscreen",
    "toggle_fullscreen",
    "_close",
]
