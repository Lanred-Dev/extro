from extro.instances.core.Instance.Audio import AudioSource


class SpatialAudioSource(AudioSource):
    def __init__(self, audio_file: str, volume: float = 1.0):
        super().__init__(audio_file=audio_file, volume=volume, is_stream=False)
