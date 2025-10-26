import pyray
from enum import IntFlag, auto
from typing import TYPE_CHECKING

import extro.internal.ComponentManager as ComponentManager
import extro.services.Audio as AudioService
import extro.services.World as WorldService
from extro.shared.Vector2C import Vector2

if TYPE_CHECKING:
    from extro.internal.systems.Transform import Transform

pyray.init_audio_device()

AUDIO_DROPOFF_DISTANCE: float = 1000.0
AUDIO_DROPOFF_RATE: float = 1.0


class AudioSourceDirtyFlags(IntFlag):
    VOLUME = auto()
    PITCH = auto()
    IS_PLAYING = auto()


def update():
    camera_position: Vector2 = (
        WorldService.camera.position if WorldService.camera else Vector2(0, 0)
    )

    for instance_id, source in ComponentManager.audio_sources.items():
        if not source._is_playing:
            continue

        if source._behavior == AudioService.AudioSourceBehaviorType.SPATIAL:
            transform: "Transform | None" = ComponentManager.transforms.get(instance_id)

            if transform:
                initial_volume: float = source._volume
                distance: float = (camera_position - transform._position).magnitude()
                dropoff_volume: float = max(
                    1 - (distance / AUDIO_DROPOFF_DISTANCE) * AUDIO_DROPOFF_RATE, 0
                )
                final_volume: float = initial_volume * dropoff_volume

                if initial_volume != final_volume:
                    source._actual_volume = final_volume
                    source.add_flag(AudioSourceDirtyFlags.VOLUME)

        if not source.is_empty():
            if source.has_flag(AudioSourceDirtyFlags.VOLUME):
                source.remove_flag(AudioSourceDirtyFlags.VOLUME)

                if source._source_type == AudioService.AudioSourceType.STREAM:
                    pyray.set_music_volume(source._audio, source._actual_volume)
                else:
                    pyray.set_sound_volume(source._audio, source._actual_volume)
            if source.has_flag(AudioSourceDirtyFlags.PITCH):
                source.remove_flag(AudioSourceDirtyFlags.PITCH)

                if source._source_type == AudioService.AudioSourceType.STREAM:
                    pyray.set_music_pitch(source._audio, source._pitch)
                else:
                    pyray.set_sound_pitch(source._audio, source._pitch)

        just_finished: bool = False

        if source.source_type == AudioService.AudioSourceType.STREAM:
            if source.has_flag(AudioSourceDirtyFlags.IS_PLAYING):
                pyray.play_music_stream(source._audio)
                source.remove_flag(AudioSourceDirtyFlags.IS_PLAYING)
            elif pyray.is_music_stream_playing(source._audio) == False:
                just_finished = True
            else:
                pyray.update_music_stream(source._audio)
        else:
            if source.has_flag(AudioSourceDirtyFlags.IS_PLAYING):
                print(source._actual_volume)
                pyray.play_sound(source._audio)
                source.remove_flag(AudioSourceDirtyFlags.IS_PLAYING)
            elif pyray.is_sound_playing(source._audio) == False:
                just_finished = True

        if just_finished:
            source._is_playing = False
            source.on_finish.fire()

            if source.remove_on_finish:
                source.destroy()


def quit():
    pyray.close_audio_device()
