from extro.instances.core.Instance import Instance
from extro.instances.core.components.AudioSource import AudioSource
import extro.services.Audio as AudioService


class Audio(Instance):
    __slots__ = Instance.__slots__ + ("source",)

    source: AudioSource

    def __init__(
        self,
        audio_file: str,
        volume: float = 1.0,
        pitch: float = 1.0,
        remove_on_finish: bool = False,
        source_type: AudioService.AudioSourceType = AudioService.AudioSourceType.EFFECT,
        behavior: AudioService.AudioSourceBehaviorType = AudioService.AudioSourceBehaviorType.NON_SPATIAL,
    ):
        super().__init__()

        source: AudioSource = AudioSource(
            self._id,
            audio_file=audio_file,
            volume=volume,
            pitch=pitch,
            remove_on_finish=remove_on_finish,
            source_type=source_type,
            behavior=behavior,
        )
        self.add_component(source)
        self.source = source
