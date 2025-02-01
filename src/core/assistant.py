import os
from ..services.audio_service import AudioService
from ..services.openai_service import OpenAIService
from ..services.tts_service import TTSService


class AIAssistant:
    def __init__(self, role, context=""):
        self.conversation_history = []
        self.role = role
        self.context = context
        self.audio_service = AudioService()
        self.openai_service = OpenAIService()
        self.tts_service = TTSService()

    def record_audio(self):
        return self.audio_service.record_audio()

    def transcribe_audio(self, audio_data, sample_rate):
        temp_file = self.audio_service.save_audio_to_temp(
            audio_data, sample_rate)
        transcript = self.openai_service.transcribe_audio(temp_file)
        os.unlink(temp_file)
        return transcript

    def get_ai_response(self, user_input):
        self.conversation_history.append(
            {"role": "user", "content": user_input})

        system_message = f"""You are a helpful {self.role} assistant.
        Additional Context: {self.context}
        Please provide concise and relevant responses."""

        messages = [
            {"role": "system", "content": system_message},
            *self.conversation_history
        ]

        ai_response = self.openai_service.get_chat_completion(messages)
        self.conversation_history.append(
            {"role": "assistant", "content": ai_response})
        return ai_response

    def text_to_speech(self, text):
        return self.tts_service.text_to_speech(text)
