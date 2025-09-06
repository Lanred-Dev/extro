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
    fps: int

    __frame_duration: float
    __last_frame_at: float
    __running: bool

    on_pre_render: Signal
    on_post_render: Signal

    def __init__(self):
        self.delta = 0
        self.set_fps(60)
        self.__last_frame_at: float = time.perf_counter()
        self.__running = True

        self.on_pre_render = Signal()
        self.on_post_render = Signal()

    def start(self):
        Console.log(f"ENGINE VERSION: ({__version__})")
        Console.log("BACKEND: pyglet")
        Console.log("AUTHOR: Landon Redmond")

        while self.__running:
            now = time.perf_counter()
            self.delta = now - (
                self.__last_frame_at if self.__last_frame_at > 0 else now
            )

            if self.delta > self.__frame_duration:
                self.__last_frame_at = now
                self.__update()

    def quit(self):
        """Exit the application."""
        Window.window.close()
        sys.exit()

    def set_fps(self, fps: int):
        """
        Set the target frames per second for the engine.

        Args:
            fps: Desired FPS.
        """
        self.fps = fps
        self.__frame_duration = 1 / self.fps

        if fps >= 100:
            Console.log(
                f"Engine FPS was set to {fps} but this engine is only capable of ~100",
                LogType.WARNING,
            )

    def __update(self):
        """Internal update function called every frame."""
        Window.window.dispatch_events()

        if Window.window.has_exit:
            self.__running = False
            return

        self.on_pre_render.fire()
        InstanceHandler.update_instances()
        CollisionHandler.update_collisions()
        Renderer.update_render()
        self.on_post_render.fire()


Engine = EngineCls()
__all__ = ["Engine"]
