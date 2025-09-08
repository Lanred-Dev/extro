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
    NONE = ["", (255, 255, 255)]


class ConsoleCls:
    _logs: List[pyglet.text.Label]
    _is_visible: bool
    _batch: pyglet.graphics.Batch
    _last_frame_at: float

    def __init__(self):
        self._logs = []
        self._batch = pyglet.graphics.Batch()
        self._is_visible = False
        self._last_frame_at = 0
        InputHandler.on_key_press.connect(self._handle_key_press)

        self._background = pyglet.shapes.Rectangle(
            x=0,
            y=0,
            width=Window.width,
            height=Window.height,
            color=(0, 0, 0, 200),
            batch=self._batch,
        )

        self._fps_label = pyglet.text.Label(
            "1000.00 fps", font_size=15, color=(255, 255, 255), batch=self._batch
        )
        self._fps_label.y = Window.height - (self._fps_label.content_height * 2)
        self._engine_version_label = pyglet.text.Label(
            __version__, font_size=15, color=(255, 255, 255), batch=self._batch
        )
        self._engine_version_label.x = (
            Window.width - self._engine_version_label.content_width
        )
        self._engine_version_label.y = (
            Window.height - self._engine_version_label.content_height
        )

    def _handle_key_press(self, key: int, mapping: List[int]):
        if key != KeyMapping.F10:
            return

        self._last_frame_at = 0
        self._is_visible = not self._is_visible

    def log(self, text: str, type: LogType = LogType.INFO):
        [prefix, color] = type.value
        self._logs.insert(
            0,
            pyglet.text.Label(
                text if type.value == LogType.NONE.value else f"[{prefix}] {text}",
                font_size=10,
                color=color,
                batch=self._batch,
            ),
        )
        self.__update_label_positions()

    def draw(self):
        if not self._is_visible:
            return

        now = time.perf_counter()
        delta = now - (self._last_frame_at if self._last_frame_at > 0 else now)
        self._last_frame_at = now
        self._fps_label.text = f"{math.floor(1.0 / delta if delta > 0 else 0)}fps"
        self._fps_label.x = Window.width - self._fps_label.content_width

        self._batch.draw()

    def __update_label_positions(self):
        current_y: float = 0

        for label in list(self._logs):
            label.position = (0, current_y, 0)
            current_y += label.content_height


Console = ConsoleCls()
__all__ = ["Console", "LogType"]
