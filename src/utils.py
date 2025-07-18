import logging
import os
import tempfile
from typing import Optional

import aiofiles
from telegram import File, InputFile, Update

from config import Config

logger = logging.getLogger(__name__)


async def download_audio_file(file: File) -> Optional[str]:
    """Download audio file from Telegram"""
    try:
        # Check file size
        if file.file_size > Config.MAX_AUDIO_SIZE_MB * 1024 * 1024:
            logger.warning(f"File too large: {file.file_size} bytes")
            return None

        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".oga")
        temp_path = temp_file.name
        temp_file.close()

        # Download file
        await file.download_to_drive(temp_path)
        logger.info(f"Audio file downloaded to: {temp_path}")

        return temp_path

    except Exception as e:
        logger.error(f"Failed to download audio file: {e}")
        return None


def cleanup_temp_file(file_path: str):
    """Clean up temporary file"""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
            logger.debug(f"Cleaned up temp file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup temp file {file_path}: {e}")


def format_transcription(text: str, processing_time: float = None) -> str:
    """Format transcription text for better readability with timing info"""
    if not text:
        return "❌ No speech detected in audio"

    # Basic formatting
    text = text.strip()
    if not text.endswith("."):
        text += "."

    # Format timing info
    timing_info = ""
    if processing_time is not None:
        timing_info = format_processing_time(processing_time)

    return f"📝 *Transcription:*\n\n{text}{timing_info}"


def format_processing_time(processing_time: float) -> str:
    """Format processing time in human-readable format with emoji"""
    if processing_time < 1.0:
        return f"\n\n⏱️ *Processing time:* {processing_time:.2f}s"
    elif processing_time < 60.0:
        return f"\n\n⏱️ *Processing time:* {processing_time:.1f}s"
    else:
        minutes = int(processing_time // 60)
        seconds = processing_time % 60
        return f"\n\n⏱️ *Processing time:* {minutes}m {seconds:.1f}s"


def get_file_info(file: File) -> str:
    """Get file information for logging"""
    size_mb = file.file_size / (1024 * 1024) if file.file_size else 0
    file_id = getattr(file, "file_id", "unknown")
    return f"File ID: {file_id}, Size: {size_mb:.2f}MB"


async def send_long_message(update: Update, text: str, processing_msg=None):
    """Send long text as file if it exceeds Telegram limits"""
    # Telegram message limit is 4096 characters
    MAX_MESSAGE_LENGTH = 4000  # Leave some buffer

    try:
        if len(text) <= MAX_MESSAGE_LENGTH:
            # Send as regular message
            if processing_msg:
                await processing_msg.edit_text(text, parse_mode="Markdown")
            else:
                await update.message.reply_text(text, parse_mode="Markdown")
        else:
            # Create temporary text file
            temp_file = tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, encoding="utf-8"
            )
            temp_file.write(text)
            temp_file.close()

            try:
                # Send file
                with open(temp_file.name, "rb") as f:
                    if processing_msg:
                        await processing_msg.edit_text(
                            "📄 Transcription too long, sending as file..."
                        )

                    await update.message.reply_document(
                        document=InputFile(f, filename="transcription.txt"),
                        caption="📝 *Audio Transcription*\n\nThe transcription was too long for a regular message.",
                    )

            finally:
                # Clean up temp file
                cleanup_temp_file(temp_file.name)

    except Exception as e:
        logger.error(f"Failed to send long message: {e}")
        error_msg = "❌ Failed to send transcription. Please try again."
        if processing_msg:
            await processing_msg.edit_text(error_msg)
        else:
            await update.message.reply_text(error_msg)
