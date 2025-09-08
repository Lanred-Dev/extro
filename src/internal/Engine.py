import time
import sys

from src.internal.Window import Window
from src.internal.Renderer import Renderer
from src.internal.CollisionHandler import CollisionHandler
from src.internal.InstanceHandler import InstanceHandler
from src.internal.components.Signal import Signal
from src.internal.Console import Console, LogType
from src.__version__ import __version__


class EngineCls:
    """
    Core engine class for managing frame updates and rendering.

    Handles delta time calculation, FPS limiting, and pre/post
    render signals.
    """

    delta: float
    _fps: int
    _frame_duration: float
    _last_frame_at: float
    _is_running: bool

    on_pre_render: Signal
    on_post_render: Signal

    def __init__(self):
        self.delta = 0
        self._fps = 60
        self._frame_duration = 1 / self._fps
        self._last_frame_at: float = time.perf_counter()
        self._is_running = False

        self.on_pre_render = Signal()
        self.on_post_render = Signal()

        # Print engine info
        Console.log("--------------------------", LogType.NONE)
        Console.log(f"ENGINE VERSION: {__version__}", LogType.NONE)
        Console.log("BACKEND: pyglet", LogType.NONE)
        Console.log("AUTHOR: Landon Redmond", LogType.NONE)
        Console.log("--------------------------", LogType.NONE)

    def start(self):
        self._is_running = True

        while self._is_running:
            now = time.perf_counter()
            self.delta = now - (self._last_frame_at if self._last_frame_at > 0 else now)

            if self.delta > self._frame_duration:
                self._last_frame_at = now
                self._update()

    def quit(self):
        """Exit the application."""
        Window.close()
        sys.exit()

    def _update(self):
        """Internal update function called every frame."""
        Window.dispatch_events()

        if Window.has_exit:
            self._is_running = False
            return

        self.on_pre_render.fire()
        InstanceHandler.update_instances()
        CollisionHandler.update_collisions()
        Renderer.render()
        self.on_post_render.fire()

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps: int):
        self._fps = fps
        self._frame_duration = 1 / self.fps


Engine = EngineCls()
__all__ = ["Engine"]
