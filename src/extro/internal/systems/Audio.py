import pyray
from enum import IntFlag, auto

import extro.internal.ComponentManager as ComponentManager
import extro.services.Audio as AudioService

pyray.init_audio_device()


class AudioSourceDirtyFlags(IntFlag):
    VOLUME = auto()
    PITCH = auto()
    IS_PLAYING = auto()


def update():
    for source in ComponentManager.audio_sources.values():
        # Cant just return because if its a stream it still has to be played/updated
        if not source.is_empty():
            if source.has_flag(AudioSourceDirtyFlags.VOLUME):
                source._actual_volume = source._volume * AudioService.global_volume
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

        if source._is_playing:
            just_finished: bool = False

            if source.source_type == AudioService.AudioSourceType.STREAM:
                if source.has_flag(AudioSourceDirtyFlags.IS_PLAYING):
                    pyray.play_music_stream(source._audio)
                    source.remove_flag(AudioSourceDirtyFlags.IS_PLAYING)
                else:
                    pyray.update_music_stream(source._audio)

                    if pyray.is_music_stream_playing(source._audio) == False:
                        just_finished = True
            else:
                if source.has_flag(AudioSourceDirtyFlags.IS_PLAYING):
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
