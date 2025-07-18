import asyncio
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import Config
from transcriber import WhisperTranscriber
from utils import (
    cleanup_temp_file,
    download_audio_file,
    format_transcription,
    get_file_info,
    send_long_message,
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, Config.LOG_LEVEL),
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)


class TranscriberBot:
    def __init__(self):
        self.transcriber = WhisperTranscriber()
        self.app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Setup bot command and message handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("about", self.about_command))
        self.app.add_handler(CommandHandler("status", self.status_command))

        # Handle voice messages
        self.app.add_handler(MessageHandler(filters.VOICE, self.handle_voice))

        # Handle audio files
        self.app.add_handler(MessageHandler(filters.AUDIO, self.handle_audio))

        # Handle document audio files
        self.app.add_handler(
            MessageHandler(filters.Document.AUDIO, self.handle_document_audio)
        )

    async def start_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = f"""
🎙️ *Welcome to Transcriber Bot!*

Transform your voice into text instantly with AI-powered transcription! 🚀

*🎯 What I can do:*
├ 🗣️ Convert voice messages to text
├ 🎵 Transcribe audio files
├ 📝 Handle long content with text files
╰⚡ Process multiple requests simultaneously

*📋 Supported formats:* {', '.join(Config.SUPPORTED_FORMATS).upper()}
*📊 Max file size:* {Config.MAX_AUDIO_SIZE_MB}MB

*🔗 Links:*
├ 📖 Commands: /help
├ ℹ️ About: /about
╰⭐ GitHub: [Give us a star!](https://github.com/Malith-Rukshan/whisper-transcriber-bot)

*👨‍💻 Developer:* @MalithRukshan
        """
        await update.message.reply_text(welcome_message, parse_mode="Markdown")

    async def help_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = f"""
📖 *Help & Commands*

*🤖 Available Commands:*
• /start - Welcome message
• /help - Show this help message
• /about - About this bot
• /status - Check bot status

*🚀 How to use:*
1. 🎙️ Send a voice message or audio file
2. ⏳ Wait for AI transcription (1-3 seconds)
3. 📝 Receive your text transcription!

*📁 Supported formats:* {', '.join(Config.SUPPORTED_FORMATS).upper()}
*📊 Max file size:* {Config.MAX_AUDIO_SIZE_MB}MB
*⚡ Features:* Concurrent processing, long text support

*💡 Tips:*
• Clear audio = better results
• Long transcriptions become text files
• Multiple users supported simultaneously

*🔗 Project:* [GitHub Repository](https://github.com/Malith-Rukshan/whisper-transcriber-bot)
        """
        await update.message.reply_text(help_message, parse_mode="Markdown")

    async def about_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        about_message = """
ℹ️ *About Whisper Transcriber Bot*

🤖 *Powered by OpenAI Whisper*
Advanced AI speech recognition technology for accurate transcription.

🔧 *Technical Details:*
├ 🧠 Model: Whisper base.en (147MB)
├ 💻 Processing: CPU-optimized inference
├ ⚡ Performance: ~1-2 seconds per audio
╰ 🌐 Platform: Docker containerized

🎯 *Features:*
├ 🎙️ Voice message transcription
├ 🎵 Multi-format audio support
├ 📝 Long text handling with files
╰ 🔄 Concurrent user processing

👨‍💻 *Developer:* @MalithRukshan
🌐 *Website:* malith.dev
📦 *Docker Hub:* [malithrukshan/whisper-transcriber-bot](https://hub.docker.com/r/malithrukshan/whisper-transcriber-bot)

🔗 *Open Source Project:*
⭐ [Star on GitHub](https://github.com/Malith-Rukshan/whisper-transcriber-bot)
🐛 [Report Issues](https://github.com/Malith-Rukshan/whisper-transcriber-bot/issues)
🤝 [Contribute](https://github.com/Malith-Rukshan/whisper-transcriber-bot/pulls)

💝 *Support the Project:*
Give us a ⭐ on GitHub if you find this useful!
        """
        await update.message.reply_text(about_message, parse_mode="Markdown")

    async def status_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        transcriber_status = "✅ Ready" if self.transcriber.is_healthy() else "❌ Error"

        status_message = f"""
🔍 *Bot Status Dashboard*

*🤖 Transcriber:* {transcriber_status}
*🧠 AI Model:* {Config.WHISPER_MODEL_NAME.upper()}
*📁 Formats:* {', '.join(Config.SUPPORTED_FORMATS).upper()}
*📊 Max Size:* {Config.MAX_AUDIO_SIZE_MB}MB
*⚡ Processing:* Concurrent
*💻 Platform:* CPU-optimized

*🚀 Performance:*
• Response time: ~1-2 seconds
• Multiple users: Supported
• Long transcriptions: Auto-file generation

*📈 Quick Stats:*
• Model size: 147MB
• Languages: English optimized
• Accuracy: High-quality AI transcription

*🔗 More info:* /about
        """
        await update.message.reply_text(status_message, parse_mode="Markdown")

    async def handle_voice(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages"""
        # Process audio concurrently without blocking other requests
        asyncio.create_task(self.process_audio(update, update.message.voice))

    async def handle_audio(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        """Handle audio files"""
        # Process audio concurrently without blocking other requests
        asyncio.create_task(self.process_audio(update, update.message.audio))

    async def handle_document_audio(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        """Handle audio files sent as documents"""
        document = update.message.document
        if document.mime_type and document.mime_type.startswith("audio/"):
            # Process audio concurrently without blocking other requests
            asyncio.create_task(self.process_audio(update, document))
        else:
            await update.message.reply_text(
                "❌ *Invalid File*\nPlease send an audio file.\n\n📁 *Supported:* MP3, M4A, WAV, OGG, FLAC\n⭐ [Star us on GitHub](https://github.com/Malith-Rukshan/whisper-transcriber-bot)",
                parse_mode="Markdown",
            )

    async def process_audio(self, update: Update, audio_file):
        """Process audio file for transcription"""
        try:
            # Send processing message
            processing_msg = await update.message.reply_text(
                "🎙️ *Transcribing audio...*\n⏳ AI is working on your audio...\n🚀 Powered by OpenAI Whisper",
                parse_mode="Markdown",
            )

            logger.info(
                f"Processing audio from user {update.effective_user.id}: {get_file_info(audio_file)}"
            )

            # Get the actual file object
            file_obj = await audio_file.get_file()

            # Download audio file
            file_path = await download_audio_file(file_obj)
            if not file_path:
                await processing_msg.edit_text(
                    "❌ *Download Failed*\nCouldn't download your audio file. Please try again!\n\n⭐ [Star us on GitHub](https://github.com/Malith-Rukshan/whisper-transcriber-bot)",
                    parse_mode="Markdown",
                )
                return

            # Transcribe audio
            transcription = await self.transcriber.transcribe_audio(file_path)

            # Send result
            if transcription:
                formatted_text = format_transcription(transcription)
                await send_long_message(update, formatted_text, processing_msg)
                logger.info(
                    f"Transcription completed for user {update.effective_user.id}"
                )
            else:
                await processing_msg.edit_text(
                    "❌ *Transcription Failed*\nCould not transcribe audio. Please try with a clearer audio file.\n\n💡 *Tips:* Use clear audio, avoid background noise\n⭐ [Star us on GitHub](https://github.com/Malith-Rukshan/whisper-transcriber-bot)",
                    parse_mode="Markdown",
                )
                logger.warning(
                    f"Transcription failed for user {update.effective_user.id}"
                )

            # Clean up temp file
            cleanup_temp_file(file_path)

        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            await update.message.reply_text(
                "❌ *Processing Error*\nAn error occurred while processing your audio. Please try again.\n\n🐛 [Report issues](https://github.com/Malith-Rukshan/whisper-transcriber-bot/issues)\n⭐ [Star us on GitHub](https://github.com/Malith-Rukshan/whisper-transcriber-bot)",
                parse_mode="Markdown",
            )

    async def run(self):
        """Run the bot"""
        try:
            Config.validate()
            logger.info(f"Starting {Config.BOT_USERNAME}...")

            if not self.transcriber.is_healthy():
                raise RuntimeError("Transcriber is not ready")

            logger.info("Bot started successfully! Press Ctrl+C to stop.")

            # Run the bot with async context manager
            async with self.app:
                await self.app.start()
                await self.app.updater.start_polling(drop_pending_updates=True)

                # Keep the bot running
                await asyncio.Event().wait()

        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise


def main():
    """Main function"""
    bot = TranscriberBot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")


if __name__ == "__main__":
    main()
