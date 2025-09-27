"""
Public facing API for the extro game engine.
"""

import pyray
from importlib.metadata import version

# pyray logs arent needed
pyray.set_trace_log_level(pyray.TraceLogLevel.LOG_NONE)

import extro.Console as Console
import extro.Window as Window
import extro.internal.Engine as Engine
from extro.shared.__shared__ import Vector2, Color, types, Coord, CoordType
import extro.utils.__utils__ as Utils
import extro.services.__services__ as Services
import extro.instances.__instances__ as Instances

# This is very very important..........
try:
    __version__ = version("extro")
except Exception:
    __version__ = "unknown"

Console.log(f"extro {__version__}")

# API Wrappers for convenience
delta = Engine.delta
quit = Engine.quit
start = Engine.start


__all__ = [
    "Console",
    "Window",
    "Vector2",
    "Color",
    "Coord",
    "CoordType",
    "types",
    "Utils",
    "Services",
    "delta",
    "quit",
    "Instances",
    "__version__",
]
