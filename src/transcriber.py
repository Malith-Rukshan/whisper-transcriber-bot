import logging
import os
import tempfile
from typing import Optional

from pywhispercpp.model import Model

from config import Config

logger = logging.getLogger(__name__)


class WhisperTranscriber:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        """Load Whisper model from downloaded file"""
        try:
            logger.info(f"Loading Whisper model from: {Config.WHISPER_MODEL_PATH}")

            # Check if model file exists
            if not os.path.exists(Config.WHISPER_MODEL_PATH):
                raise FileNotFoundError(
                    f"Model file not found: {Config.WHISPER_MODEL_PATH}"
                )

            # Load model from file path (not download automatically)
            self.model = Model(Config.WHISPER_MODEL_PATH, n_threads=6)

            # Test if the model is working by checking if it can be used
            if hasattr(self.model, "transcribe"):
                logger.info(
                    "Whisper model loaded successfully and ready for transcription"
                )
            else:
                logger.error("Model loaded but transcribe method not available")
                self.model = None
                raise RuntimeError("Model not properly initialized")

        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.model = None
            raise

    async def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio file to text"""
        try:
            logger.info(f"Starting transcription of: {audio_file_path}")

            # Transcribe audio
            segments = self.model.transcribe(audio_file_path)

            # Combine all segments into single text
            full_text = ""
            for segment in segments:
                full_text += segment.text + " "

            full_text = full_text.strip()

            if full_text:
                logger.info("Transcription completed successfully")
                return full_text
            else:
                logger.warning("Transcription returned empty result")
                return None

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None

    def is_healthy(self) -> bool:
        """Check if transcriber is ready"""
        return self.model is not None
