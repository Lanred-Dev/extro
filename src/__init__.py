from src.internal.Engine import Engine
from src.internal.InputHandler import InputHandler, KeyMapping, MouseButtonMapping
from src.internal.Console import Console, LogType
import src.instances as Instances
import src.animation as Animation
from src.values.Color import Color
from src.values.Vector2 import Vector2
from src.__version__ import __version__


def start():
    Engine.start()


__all__ = [
    "start",
    "Instances",
    "Animation",
    "InputHandler",
    "KeyMapping",
    "MouseButtonMapping",
    "Console",
    "LogType",
    "Color",
    "Vector2",
    "__version__",
]
