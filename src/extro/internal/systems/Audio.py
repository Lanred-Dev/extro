import pyray
from typing import TYPE_CHECKING

import extro.internal.InstanceManager as InstanceManager
from extro.internal.utils.InstanceRegistry import InstanceRegistry

if TYPE_CHECKING:
    from extro.instances.core.Instance.Audio import AudioSource

pyray.init_audio_device()

global_volume: float = 1.0
sources: InstanceRegistry = InstanceRegistry("Audio System")


def update():
    for source_id in sources.instances[:]:
        source: "AudioSource" = InstanceManager.instances[source_id]  # type: ignore

        if not source._is_playing:
            continue

        if source._is_stream:
            pyray.update_music_stream(source._audio)

            if not pyray.is_music_stream_playing(source._audio):
                source.on_finish.fire()
        elif not pyray.is_sound_playing(source._audio):
            source._is_playing = False
            source.on_finish.fire()


def quit():
    pyray.close_audio_device()
