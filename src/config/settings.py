import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SAMPLE_RATE = 44100
    RECORDING_DURATION = 5
    AI_MODEL = "gpt-3.5-turbo"
    WHISPER_MODEL = "whisper-1"
    LANGUAGE = "en"


settings = Settings()
