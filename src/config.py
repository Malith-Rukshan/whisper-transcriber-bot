import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Telegram Bot Settings
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "TranscriberXBOT")

    # Whisper Model Settings
    WHISPER_MODEL_PATH = os.getenv("WHISPER_MODEL_PATH", "../models/ggml-base.en.bin")
    WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "base.en")

    # Bot Limits
    MAX_AUDIO_SIZE_MB = int(os.getenv("MAX_AUDIO_SIZE_MB", "50"))
    SUPPORTED_FORMATS = os.getenv("SUPPORTED_FORMATS", "mp3,m4a,wav,ogg,flac").split(
        ","
    )

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        # Check if the downloaded model file exists
        if not os.path.exists(cls.WHISPER_MODEL_PATH):
            raise ValueError(
                f"Whisper model file not found: {cls.WHISPER_MODEL_PATH}. Please run ./download_model.sh first."
            )
