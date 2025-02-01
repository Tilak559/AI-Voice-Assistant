from openai import OpenAI
from ..config.settings import settings


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def transcribe_audio(self, audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model=settings.WHISPER_MODEL,
                file=audio_file
            )
        return transcript.text

    def get_chat_completion(self, messages):
        response = self.client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=messages
        )
        return response.choices[0].message.content
