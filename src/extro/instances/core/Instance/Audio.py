import pyray
from typing import Any

import extro.internal.systems.Audio as AudioSystem
from extro.utils.Signal import Signal
import extro.Console as Console
import extro.internal.services.FileCache as FileCacheService
from extro.instances.core.Instance import Instance


class AudioSource(Instance):
    __slots__ = Instance.__slots__ + (
        "_volume",
        "_actual_volume",
        "_pitch",
        "_audio_file",
        "_audio",
        "_is_stream",
        "_is_playing",
        "_started_at",
        "on_finish",
    )

    _volume: float
    _actual_volume: float
    _pitch: float
    _audio_file: str
    # Its easier to just cast this to Any rather than check the type all the time, when `_is_stream` is known
    _audio: Any
    _is_stream: bool
    _is_playing: bool
    _started_at: float

    on_finish: Signal

    def __init__(
        self,
        audio_file: str,
        is_stream: bool = False,
        volume: float = 1.0,
        pitch: float = 1.0,
    ):
        self._audio_file = audio_file
        self._is_stream = is_stream
        self._volume = volume
        self._pitch = pitch
        self._is_playing = False
        self._started_at = 0

        self.on_finish = Signal()
        self._janitor.add(self.on_finish)

        self._load_audio()
        self._recalculate_volume()
        self._janitor.add(self._unload_audio)

        AudioSystem.sources.register(self._id)
        self._janitor.add(AudioSystem.sources.unregister, self._id)

    def play(self):
        """Plays the audio source from the start. If it's already playing, it restarts it."""
        if self._is_stream:
            pyray.play_music_stream(self._audio)
        else:
            pyray.play_sound(self._audio)

        self._is_playing = True
        self._started_at = pyray.get_time()

    def stop(self):
        """Stops the audio source if it's playing."""
        if not self._is_playing:
            Console.log(
                f"Cannot stop audio source {self._id} because it is not playing",
                Console.LogType.WARNING,
            )
            return

        if self._is_stream:
            pyray.stop_music_stream(self._audio)
            pyray.seek_music_stream(self._audio, 0.0)
        else:
            pyray.stop_sound(self._audio)

        self._is_playing = False

    def pause(self):
        """Pauses the audio source if it's playing."""
        if not self._is_playing:
            Console.log(
                f"Cannot pause audio source {self._id} because it is not playing",
                Console.LogType.WARNING,
            )
            return

        if self._is_stream:
            pyray.pause_music_stream(self._audio)
        else:
            pyray.stop_sound(self._audio)

        self._is_playing = False

    def _recalculate_volume(self):
        self._actual_volume = self._volume * AudioSystem.global_volume
        self._apply_volume()

    def _load_audio(self):
        self._unload_audio()

        if self._is_stream:
            self._audio = pyray.load_music_stream(self._audio_file)
        else:
            self._audio = FileCacheService.audio_cache.load(self._audio_file)

        self._apply_pitch()
        self._apply_volume()

    def _unload_audio(self):
        if not getattr(self, "_audio", None):
            return

        if self._is_stream:
            pyray.unload_music_stream(self._audio)
        else:
            pyray.unload_sound(self._audio)
            FileCacheService.audio_cache.unload(self._audio_file)

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, volume: float):
        self._volume = volume
        self._recalculate_volume()

    @property
    def pitch(self) -> float:
        return self._pitch

    @pitch.setter
    def pitch(self, pitch: float):
        self._pitch = pitch

    def _apply_volume(self):
        if self._is_stream:
            pyray.set_music_volume(self._audio, self._actual_volume)
        else:
            pyray.set_sound_volume(self._audio, self._actual_volume)

    def _apply_pitch(self):
        if self._is_stream:
            pyray.set_music_pitch(self._audio, self._pitch)
        else:
            pyray.set_sound_pitch(self._audio, self._pitch)
