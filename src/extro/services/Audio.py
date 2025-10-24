from enum import Enum, auto

import extro.internal.systems.Audio as AudioSystem
import extro.internal.ComponentManager as ComponentManager


global_volume: float = 0.0


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

    for source in ComponentManager.audio_sources.values():
        source.add_flag(AudioSystem.AudioSourceDirtyFlags.VOLUME)


__all__ = [
    "global_volume",
    "set_global_volume",
    "AudioSourceType",
    "AudioSourceBehaviorType",
]
