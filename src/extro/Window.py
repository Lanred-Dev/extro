"""Provides controls for managing the game window."""

import pyray

from extro.shared.Vector2 import Vector2
from extro.utils.Signal import Signal

_PRIMARY_MONITOR_INDEX: int = pyray.get_current_monitor()

title: str = "extro engine"
size: Vector2 = Vector2(500, 500)
is_fullscreen: bool = False
on_resize: Signal = Signal()

# Window configuration
pyray.set_config_flags(pyray.ConfigFlags.FLAG_MSAA_4X_HINT)
pyray.set_config_flags(pyray.ConfigFlags.FLAG_WINDOW_HIGHDPI)
pyray.init_window(int(size.x), int(size.y), title)
pyray.set_window_state(pyray.ConfigFlags.FLAG_WINDOW_ALWAYS_RUN)


def set_title(title: str):
    """Set the window title."""
    pyray.set_window_title(title)


def set_size(new_size: Vector2):
    """Set the window size."""
    global size
    size = new_size
    pyray.set_window_size(int(new_size.x), int(new_size.y))
    on_resize.fire(new_size)


def toggle_fullscreen():
    """Toggle fullscreen mode."""
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    set_size(
        Vector2(
            pyray.get_monitor_width(_PRIMARY_MONITOR_INDEX),
            pyray.get_monitor_height(_PRIMARY_MONITOR_INDEX),
        )
        if is_fullscreen
        else size
    )
    pyray.toggle_fullscreen()


def close():
    """
    Close the window.

    This is automatically called on engine shutdown. You do not need to call this manually, but if needed you can.
    """
    pyray.close_window()


__all__ = [
    "title",
    "size",
    "is_fullscreen",
    "set_title",
    "set_size",
    "toggle_fullscreen",
    "close",
]
