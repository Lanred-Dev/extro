import pyray

from src.values.Vector2 import Vector2

PRIMARY_MONITOR_INDEX: int = 0


class WindowCls:
    """
    Wrapper for the application window using raylib.
    """

    _title: str
    _size: Vector2
    _actual_size: Vector2

    def __init__(
        self,
        size: Vector2 = Vector2(900, 900),
        title: str = "extro engine",
        fullscreen: bool = False,
    ):
        self._title = title
        self._size = size
        self._actual_size = size

        pyray.init_window(int(size.x), int(size.y), title)
        pyray.set_window_state(pyray.ConfigFlags.FLAG_WINDOW_ALWAYS_RUN)
        pyray.set_window_state(pyray.ConfigFlags.FLAG_MSAA_4X_HINT)
        pyray.set_window_state(pyray.ConfigFlags.FLAG_WINDOW_HIGHDPI)

        if fullscreen:
            self.toggle_fullscreen()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title
        pyray.set_window_title(title)

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, size: Vector2):
        self._size = size
        self._actual_size = size
        pyray.set_window_size(int(size.x), int(size.y))

    def is_fullscreen(self) -> bool:
        return pyray.is_window_fullscreen()

    def toggle_fullscreen(self):
        if self.is_fullscreen():
            pyray.set_window_size(int(self._size.x), int(self._size.y))
        else:
            self._actual_size = Vector2(
                pyray.get_monitor_width(PRIMARY_MONITOR_INDEX),
                pyray.get_monitor_height(PRIMARY_MONITOR_INDEX),
            )
            pyray.set_window_size(int(self._actual_size.x), int(self._actual_size.y))

        pyray.toggle_fullscreen()


Window = WindowCls()
__all__ = ["Window"]
