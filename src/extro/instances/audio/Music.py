from extro.instances.core.Instance.Audio import Audio
import extro.services.Audio as AudioService


class MusicAudio(Audio):
    def __init__(
        self,
        audio_file: str,
        volume: float = 1.0,
        pitch: float = 1.0,
        remove_on_finish: bool = False,
        behavior: AudioService.AudioSourceBehaviorType = AudioService.AudioSourceBehaviorType.NON_SPATIAL,
    ):
        super().__init__(
            audio_file=audio_file,
            volume=volume,
            pitch=pitch,
            remove_on_finish=remove_on_finish,
            source_type=AudioService.AudioSourceType.STREAM,
            behavior=behavior,
        )
