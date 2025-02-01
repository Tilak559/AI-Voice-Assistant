import tempfile
from scipy.io.wavfile import write
import sounddevice as sd
from ..config.settings import settings


class AudioService:
    @staticmethod
    def record_audio():
        recording = sd.rec(
            int(settings.RECORDING_DURATION * settings.SAMPLE_RATE),
            samplerate=settings.SAMPLE_RATE,
            channels=1
        )
        sd.wait()
        return recording, settings.SAMPLE_RATE

    @staticmethod
    def save_audio_to_temp(audio_data, sample_rate):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            write(temp_audio.name, sample_rate, audio_data)
            return temp_audio.name
