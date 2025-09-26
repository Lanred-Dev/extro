import pyray
from typing import TYPE_CHECKING

import extro.Console as Console
import extro.internal.services.Identity as IdentityService

if TYPE_CHECKING:
    from extro.core.AudioSource import AudioSource

pyray.init_audio_device()

global_volume: float = 1.0

instances: "dict[str, AudioSource]" = {}


def register(source: "AudioSource"):
    if source in instances:
        Console.log("Audio source is already registered", Console.LogType.WARNING)
        return

    id: str = IdentityService.generate_id(10, "i_")
    source._id = id
    instances[id] = source
    Console.log(f"Audio source {id} is now registered", Console.LogType.DEBUG)


def unregister(source_id: str):
    if source_id not in instances:
        Console.log("Audio source is not registered", Console.LogType.WARNING)
        return

    del instances[source_id]
    Console.log(
        f"Audio source {source_id} is no longer registered", Console.LogType.DEBUG
    )


def update():
    for source in instances.values():
        if not source._is_playing:
            continue

        if source._is_stream:
            pyray.update_music_stream(source._audio)

            if not pyray.is_music_stream_playing(source._audio):
                source.on_finish.fire()
        else:
            if not pyray.is_sound_playing(source._audio):
                source._is_playing = False
                source.on_finish.fire()


def quit():
    pyray.close_audio_device()
