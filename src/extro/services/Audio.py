import extro.internal.systems.Audio as AudioSystem


global_volume: float = 1.0


def set_global_volume(volume: float):
    """Sets the global volume for all audio sources."""
    global global_volume
    global_volume = max(0.0, min(1.0, volume))

    for source in AudioSystem.instances.values():
        source._recalculate_volume()


__all__ = ["global_volume", "set_global_volume"]
