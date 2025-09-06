from src.values.Vector2 import Vector2
import pyglet


class WindowCls:
    """
    Wrapper for the application window using pyglet.

    Provides helper methods to set title, size, and fullscreen mode.
    """

    def __init__(self):
        """Initialize the window."""
        self.window = pyglet.window.Window(800, 600, "Manual Rendering Window")

    def set_title(self, text: str):
        """
        Set the title of the window.

        Args:
            text: The window title string.
        """
        self.window.set_caption(text)

    def set_size(self, size: Vector2):
        """
        Resize the window to the specified dimensions.

        Args:
            size: A Vector2 containing width (x) and height (y).
        """
        self.window.set_size(int(size.x), int(size.y))

    def set_full_screen(self, fullscreen: bool):
        """
        Enable or disable fullscreen mode.

        Args:
            fullscreen: True to enable fullscreen, False to disable.
        """
        self.window.set_fullscreen(fullscreen)


Window = WindowCls()
__all__ = ["Window"]
