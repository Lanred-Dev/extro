import pyray

pyray.set_trace_log_level(pyray.TraceLogLevel.LOG_NONE)

import src.internal.Engine as Engine
import src.internal.InputHandler as InputHandler
import src.internal.Console as Console
import src.instances as Instances
import src.animation as Animation
import src.internal.Renderer as Renderer
from src.internal.Window import Window
from src.values.Color import Color
from src.values.Vector2 import Vector2
from src.__version__ import __version__


# Print engine info
Console.log("--------------------------", Console.LogType.NONE)
Console.log(f"ENGINE VERSION: {__version__}", Console.LogType.NONE)
Console.log("AUTHOR: Landon Redmond", Console.LogType.NONE)
Console.log("--------------------------", Console.LogType.NONE)

__all__ = [
    "Engine",
    "Instances",
    "Animation",
    "InputHandler",
    "Console",
    "Color",
    "Vector2",
    "__version__",
    "Window",
    "Renderer",
]
