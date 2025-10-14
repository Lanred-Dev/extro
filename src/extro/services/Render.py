import pyray

from extro import Console
from extro.shared.types import RenderTargetType

fps: int = 60


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
]
