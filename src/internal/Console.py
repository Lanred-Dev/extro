from typing import List, Tuple
import time
import pyray
from enum import Enum

from src.__version__ import __version__
from src.internal.Window import Window
from src.instances.ui.Fonts import Arial


class LogType(Enum):
    ERROR = ["Error", (255, 0, 0, 255)]
    INFO = ["Info", (255, 255, 255, 255)]
    WARNING = ["Warning", (255, 255, 0, 255)]
    NONE = ["", (255, 255, 255, 255)]


_logs: List[Tuple[Tuple[int, int, int, int], str]] = []
_is_visible: bool = False
_last_frame_at: float = time.perf_counter()


def log(text: str, type: LogType = LogType.INFO):
    global _logs
    [prefix, color] = type.value
    _logs.insert(
        0, (color, text if type.value == LogType.NONE.value else f"[{prefix}] {text}")
    )
    _logs = _logs[:20]


def _draw():
    global _is_visible, _last_frame_at

    if pyray.is_key_pressed(pyray.KeyboardKey.KEY_F10):
        _is_visible = not _is_visible

    if not _is_visible:
        return

    now = time.perf_counter()
    delta = now - (_last_frame_at if _last_frame_at > 0 else now)
    _last_frame_at = now

    pyray.draw_rectangle(
        0, 0, int(Window._actual_size.x), int(Window._actual_size.y), (0, 0, 0, 150)
    )

    fps_text: str = f"{1 / delta:.0f} FPS"
    fps_label_width: pyray.Vector2 = pyray.measure_text_ex(Arial._font, fps_text, 20, 1)
    pyray.draw_text_ex(
        Arial._font,
        fps_text,
        (int(Window._actual_size.x) - fps_label_width.x, 0),
        20,
        1,
        (255, 255, 255, 255),
    )

    for index, (color, text) in enumerate(_logs):
        pyray.draw_text_ex(
            Arial._font,
            text,
            (0, int(Window._actual_size.y - ((index + 1) * 20))),
            20,
            1,
            color,
        )


__all__ = ["LogType", "log", "_draw"]
