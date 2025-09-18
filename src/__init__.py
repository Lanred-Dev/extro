import pyray

pyray.set_trace_log_level(pyray.TraceLogLevel.LOG_NONE)

import src.internal.Engine as Engine
import src.internal.services.InputService as InputService
import src.internal.services.WorldService as WorldService
import src.internal.services.ScreenService as ScreenService
import src.internal.Console as Console
import src.instances as Instances
import src.animation as Animation
import src.internal.handlers.Renderer as Renderer
import src.internal.Window as Window
from src.internal.helpers.Timeout import Timeout
from src.values.Color import Color
from src.values.Vector2 import Vector2
from src.__version__ import __version__


# Print engine info
Console.log("--------------------------", Console.LogType.NONE)
Console.log(f"ENGINE VERSION: {__version__}", Console.LogType.NONE)
Console.log("BUILD DATE: N/A", Console.LogType.NONE)
Console.log("--------------------------", Console.LogType.NONE)

__all__ = [
    "Engine",
    "Instances",
    "Animation",
    "InputService",
    "WorldService",
    "ScreenService",
    "Console",
    "Color",
    "Vector2",
    "__version__",
    "Window",
    "Renderer",
    "Timeout",
]
