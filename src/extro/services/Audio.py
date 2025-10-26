from enum import Enum, auto
import pyray


global_volume: float = 1.0


class AudioSourceType(Enum):
    EFFECT = auto()
    STREAM = auto()


class AudioSourceBehaviorType(Enum):
    SPATIAL = auto()
    NON_SPATIAL = auto()


def set_global_volume(volume: float):
    """Sets the global volume for all audio sources."""
    global global_volume
    global_volume = max(0.0, min(1.0, volume))
    pyray.set_master_volume(global_volume)


__all__ = [
    "global_volume",
    "set_global_volume",
    "AudioSourceType",
    "AudioSourceBehaviorType",
]
