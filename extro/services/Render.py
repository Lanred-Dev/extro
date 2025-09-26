import pyray

from extro import Console
from extro.shared.types import RenderTargetType
from extro.utils.Signal import Signal

fps: int = 60
on_pre_render: Signal = Signal()
on_post_render: Signal = Signal()


def set_fps(new_fps: int):
    """Set the target FPS."""
    if new_fps <= 0:
        Console.log("FPS must be greater than 0", Console.LogType.WARNING)
        return

    global fps
    fps = new_fps
    pyray.set_target_fps(new_fps)
    Console.log(f"Target FPS set to {new_fps}")


def get_fps() -> int:
    """Get the current FPS."""
    return pyray.get_fps()


__all__ = [
    "fps",
    "set_fps",
    "get_fps",
    "RenderTargetType",
    "on_pre_render",
    "on_post_render",
]
