from enum import Enum
import pyglet
import time
import math
from src.internal.InputHandler import InputHandler, KeyMapping
from src.internal.Window import Window
from src.__version__ import __version__
from typing import List


class LogType(Enum):
    ERROR = ["Error", (255, 0, 0)]
    INFO = ["Info", (255, 255, 255)]
    WARNING = ["Warning", (255, 255, 0)]


class ConsoleCls:
    __labels: List[pyglet.text.Label]
    __visible: bool
    __batch: pyglet.graphics.Batch
    __last_frame_at: float

    def __init__(self):
        self.__labels = []
        self.__batch = pyglet.graphics.Batch()
        self.__visible = False
        self.__last_frame_at = 0
        InputHandler.on_key_press.connect(self.__toggle_visiblity)

        self.__background = pyglet.shapes.Rectangle(
            x=0,
            y=0,
            width=Window.window.width,
            height=Window.window.height,
            color=(0, 0, 0, 200),
            batch=self.__batch,
        )

        self.__fps_label = pyglet.text.Label(
            "1000.00 fps", font_size=15, color=(255, 255, 255), batch=self.__batch
        )
        self.__fps_label.y = Window.window.height - (
            self.__fps_label.content_height * 2
        )
        self.__engine_version_label = pyglet.text.Label(
            __version__, font_size=15, color=(255, 255, 255), batch=self.__batch
        )
        self.__engine_version_label.x = (
            Window.window.width - self.__engine_version_label.content_width
        )
        self.__engine_version_label.y = (
            Window.window.height - self.__engine_version_label.content_height
        )

    def __toggle_visiblity(self, key: int, mapping: List[int]):
        if key != KeyMapping.F10:
            return

        self.__last_frame_at = 0
        self.__visible = not self.__visible

    def log(self, text: str, type: LogType = LogType.INFO):
        [prefix, color] = type.value
        self.__labels.insert(
            0,
            pyglet.text.Label(
                f"[{prefix}] {text}",
                font_size=10,
                color=color,
                batch=self.__batch,
            ),
        )
        self.__update_label_positions()

    def draw(self):
        if not self.__visible:
            return

        now = time.perf_counter()
        delta = now - (self.__last_frame_at if self.__last_frame_at > 0 else now)
        self.__last_frame_at = now
        self.__fps_label.text = f"{math.floor(1.0 / delta if delta > 0 else 0)}fps"
        self.__fps_label.x = Window.window.width - self.__fps_label.content_width

        self.__batch.draw()

    def __update_label_positions(self):
        current_y: float = 0

        for label in list(self.__labels):
            label.position = (0, current_y, 0)
            current_y += label.content_height


Console = ConsoleCls()
__all__ = ["Console", "LogType"]
