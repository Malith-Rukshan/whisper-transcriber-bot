import os

from dotenv import load_dotenv

load_dotenv()


def get_model_path():
    """Get the correct model path based on current working directory"""
    env_path = os.getenv("WHISPER_MODEL_PATH")
    if env_path:
        return env_path
    
    # Try different possible paths
    possible_paths = [
        "models/ggml-base.en.bin",      # Docker container
        "../models/ggml-base.en.bin",   # Running from src/
        "./models/ggml-base.en.bin",    # Running from root
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Default to the first path if none exist
    return possible_paths[0]


class Config:
    # Telegram Bot Settings
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "TranscriberXBOT")

    # Whisper Model Settings
    WHISPER_MODEL_PATH = get_model_path()
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
            # Provide detailed error for debugging
            cwd = os.getcwd()
            available_files = []
            for root, _, files in os.walk('.'):
                for file in files:
                    if 'ggml-base.en.bin' in file:
                        available_files.append(os.path.join(root, file))
            
            error_msg = f"""
Whisper model file not found: {cls.WHISPER_MODEL_PATH}
Current working directory: {cwd}
Available model files found: {available_files or 'None'}

Troubleshooting:
1. For Docker: Ensure 'RUN ./download_model.sh' is in Dockerfile
2. For local: Run './download_model.sh' to download model
3. Check WHISPER_MODEL_PATH environment variable
"""
            raise ValueError(error_msg)
