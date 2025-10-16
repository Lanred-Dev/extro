"""
Public facing API for the extro game engine.
"""

import pyray

# pyray logs arent needed
pyray.set_trace_log_level(pyray.TraceLogLevel.LOG_NONE)

import extro.Console as Console
import extro.Window as Window
import extro.internal.Engine as Engine
import extro.assets.__assets__ as Assets
from extro.shared.__shared__ import Vector2, RGBAColor, types, Coord, CoordType
import extro.utils.__utils__ as Utils
import extro.services.__services__ as Services
import extro.instances.__instances__ as Instances
import extro.animation.__animation__ as Animation

# API Wrappers for convenience
quit = Engine.quit
start = Engine.start


__all__ = [
    "Console",
    "Window",
    "Vector2",
    "RGBAColor",
    "Coord",
    "CoordType",
    "types",
    "Utils",
    "Services",
    "quit",
    "Instances",
    "Assets",
    "Animation",
]
