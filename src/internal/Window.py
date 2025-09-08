import pyglet


class WindowCls(pyglet.window.Window):
    """
    Wrapper for the application window using pyglet.
    """

    def set_title(self, text: str):
        """
        Set the title of the window.

        Args:
            text: The window title string.
        """
        self.set_caption(text)


Window = WindowCls(caption="extro engine")
__all__ = ["Window"]
