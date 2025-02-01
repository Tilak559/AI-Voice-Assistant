from io import BytesIO
from gtts import gTTS
from ..config.settings import settings


class TTSService:
    @staticmethod
    def text_to_speech(text):
        tts = gTTS(text=text, lang=settings.LANGUAGE)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
