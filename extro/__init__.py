"""
Public facing API for the extro game engine.
"""

import pyray

# pyray logs arent needed
pyray.set_trace_log_level(pyray.TraceLogLevel.LOG_NONE)

import extro.Console as Console
import extro.Window as Window
import extro.internal.Engine as Engine
from extro.shared.__shared__ import Vector2, Color, types, Coord, CoordType
import extro.utils.__utils__ as utils
import extro.services.__services__ as services
import extro.instances as Instances
from extro.__version__ import __version__


# Print engine info
Console.log(f"extro {__version__}")

# API Wrappers for convenience
delta = Engine.delta
quit = Engine.quit


__all__ = [
    "Console",
    "Window",
    "Vector2",
    "Color",
    "Coord",
    "CoordType",
    "types",
    "utils",
    "services",
    "delta",
    "quit",
    "Instances",
    "__version__",
]
