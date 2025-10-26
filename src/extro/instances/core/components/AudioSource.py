import pyray
from typing import TYPE_CHECKING, Any

from extro.instances.core.components.Component import Component
import extro.internal.ComponentManager as ComponentManager
import extro.internal.systems.Audio as AudioSystem
import extro.services.Audio as AudioService
from extro.utils.Signal import Signal

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager


class AudioSource(Component):
    __slots__ = Component.__slots__ + (
        "_volume",
        "_pitch",
        "_is_playing",
        "remove_on_finish",
        "_source_type",
        "_behavior",
        "_audio_file",
        "_audio",
        "_actual_volume",
        "on_finish",
    )

    _key = "audio_source"

    _volume: float
    _pitch: float
    _is_playing: bool
    remove_on_finish: bool
    _source_type: AudioService.AudioSourceType
    _behavior: AudioService.AudioSourceBehaviorType
    _audio_file: str
    _audio: Any  # Easier to cast to Any, the type is checked based on `_source_type`
    _actual_volume: float
    on_finish: Signal

    def __init__(
        self,
        owner: "InstanceManager.InstanceIDType",
        audio_file: str,
        volume: float = 1.0,
        pitch: float = 1.0,
        remove_on_finish: bool = False,
        source_type: AudioService.AudioSourceType = AudioService.AudioSourceType.EFFECT,
        behavior: AudioService.AudioSourceBehaviorType = AudioService.AudioSourceBehaviorType.NON_SPATIAL,
    ):
        super().__init__(owner, ComponentManager.ComponentType.AUDIO_SOURCE)

        self._volume = volume
        self._actual_volume = volume
        self._pitch = pitch
        self._is_playing = False
        self.remove_on_finish = remove_on_finish
        self._source_type = source_type
        self._behavior = behavior
        self.on_finish = Signal()
        self._audio_file = audio_file

        self._load()

    def destroy(self):
        super().destroy()
        self._unload()

    def _load(self):
        if self._source_type == AudioService.AudioSourceType.STREAM:
            self._audio = pyray.load_music_stream(self._audio_file)
        else:
            self._audio = pyray.load_sound(self._audio_file)

        self.add_flag(AudioSystem.AudioSourceDirtyFlags.VOLUME)
        self.add_flag(AudioSystem.AudioSourceDirtyFlags.PITCH)

    def _unload(self):
        if self._source_type == AudioService.AudioSourceType.STREAM:
            pyray.unload_music_stream(self._audio)
        else:
            pyray.unload_sound(self._audio)

    @property
    def source_type(self) -> AudioService.AudioSourceType:
        return self._source_type

    @property
    def behavior(self) -> AudioService.AudioSourceBehaviorType:
        return self._behavior

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, volume: float):
        self._volume = volume
        self.add_flag(AudioSystem.AudioSourceDirtyFlags.VOLUME)

    @property
    def pitch(self) -> float:
        return self._pitch

    @pitch.setter
    def pitch(self, pitch: float):
        self._pitch = pitch
        self.add_flag(AudioSystem.AudioSourceDirtyFlags.PITCH)

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    def play(self):
        self._is_playing = True
        self.add_flag(AudioSystem.AudioSourceDirtyFlags.IS_PLAYING)

    def stop(self):
        self._is_playing = False
        self.add_flag(AudioSystem.AudioSourceDirtyFlags.IS_PLAYING)
