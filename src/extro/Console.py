"""Built-in in-game console for logging messages, displaying debug information, and monitoring performance."""

import time
import pyray
from enum import Enum

import extro.Window as Window
from extro.assets.Fonts import Arial
from extro.shared.RGBAColorC import RGBAColor
import extro.Profiler as Profiler


class LogPriority(Enum):
    DEBUG = 3
    WARNING = 2
    ERROR = 1
    NONE = 0


class LogType(Enum):
    DEBUG = [LogPriority.DEBUG, "Debug", RGBAColor(255, 255, 255)]
    WARNING = [LogPriority.WARNING, "Warning", RGBAColor(255, 255, 0)]
    ERROR = [LogPriority.ERROR, "Error", RGBAColor(255, 0, 0)]


logs: list[tuple[LogType, str]] = []
is_visible: bool = False
is_enabled: bool = True
last_frame_at: float = time.perf_counter()
max_log_count: int = 25
log_priority: LogPriority = LogPriority.DEBUG


def _trim_logs():
    """Trim the logs to the maximum log count and remove logs above the current priority."""
    global logs

    for log in list(logs):
        [priority, _, _] = log[0].value

        if priority.value > log_priority.value:
            logs.remove(log)

    if len(logs) > max_log_count:
        logs = logs[:max_log_count]


def log(text: str, type: LogType = LogType.DEBUG):
    """Print a message to the console."""
    if not is_enabled:
        return

    global logs

    [priority, _, _] = type.value

    # No need to save logs that are above the current log priority
    if priority.value > log_priority.value:
        return

    logs.insert(0, (type, text))
    _trim_logs()


def _draw():
    if not is_enabled:
        return

    global is_visible, last_frame_at

    if pyray.is_key_pressed(pyray.KeyboardKey.KEY_F10):
        is_visible = not is_visible

    if not is_visible:
        return

    # Background
    pyray.draw_rectangle(0, 0, int(Window.size.x), int(Window.size.y), (0, 0, 0, 150))

    for index, (type, text) in enumerate(logs):
        [_, prefix, color] = type.value
        pyray.draw_text_ex(
            Arial._font,
            f"[{prefix}]: {text}",
            (0, int(Window.size.y - ((index + 1) * 20))),
            20,
            1,
            color.to_tuple(),
        )

    # FPS counter
    fps_text: str = f"{pyray.get_fps()} FPS"
    fps_label_size: pyray.Vector2 = pyray.measure_text_ex(Arial._font, fps_text, 20, 1)
    fps_label_x: int = int(Window.size.x) - int(fps_label_size.x)
    pyray.draw_rectangle(
        fps_label_x - 5,
        0,
        int(fps_label_size.x) + 10,
        int(fps_label_size.y) + 10,
        (0, 0, 0, 255),
    )
    pyray.draw_text_ex(
        Arial._font,
        fps_text,
        (fps_label_x, 5),
        20,
        1,
        (255, 255, 255, 255),
    )

    Profiler._draw()


def set_log_priority(priority: LogPriority):
    """Set the current log priority. Logs above this priority will not be shown."""
    global log_priority
    log_priority = priority
    _trim_logs()


def set_max_log_count(count: int):
    """Set the maximum number of logs to keep in memory."""
    global max_log_count, logs
    max_log_count = count
    _trim_logs()


__all__ = [
    "is_enabled",
    "LogType",
    "LogPriority",
    "log",
    "set_log_priority",
    "set_max_log_count",
    "_draw",
]
