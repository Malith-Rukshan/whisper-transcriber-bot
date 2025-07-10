import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from bot import TranscriberBot


class TestTranscriberBot(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Mock the config to avoid requiring actual bot token
        self.config_patcher = patch("bot.Config")
        self.mock_config = self.config_patcher.start()
        self.mock_config.TELEGRAM_BOT_TOKEN = "test_token"
        self.mock_config.validate.return_value = None

        # Mock the transcriber
        self.transcriber_patcher = patch("bot.WhisperTranscriber")
        self.mock_transcriber_class = self.transcriber_patcher.start()
        self.mock_transcriber = Mock()
        self.mock_transcriber.is_healthy.return_value = True
        self.mock_transcriber_class.return_value = self.mock_transcriber

        # Create bot instance
        self.bot = TranscriberBot()

    def tearDown(self):
        """Clean up after tests"""
        self.config_patcher.stop()
        self.transcriber_patcher.stop()

    def test_bot_initialization(self):
        """Test bot initializes correctly"""
        self.assertIsNotNone(self.bot.app)
        self.assertIsNotNone(self.bot.transcriber)

    def test_start_command(self):
        """Test /start command response"""
        mock_update = Mock()
        mock_message = Mock()
        mock_message.reply_text = AsyncMock()
        mock_update.message = mock_message

        # Run the command
        asyncio.run(self.bot.start_command(mock_update, None))

        # Verify response
        mock_message.reply_text.assert_called_once()
        args, kwargs = mock_message.reply_text.call_args
        self.assertIn("Welcome to", args[0])
        self.assertEqual(kwargs.get("parse_mode"), "Markdown")

    def test_help_command(self):
        """Test /help command response"""
        mock_update = Mock()
        mock_message = Mock()
        mock_message.reply_text = AsyncMock()
        mock_update.message = mock_message

        # Run the command
        asyncio.run(self.bot.help_command(mock_update, None))

        # Verify response
        mock_message.reply_text.assert_called_once()
        args, kwargs = mock_message.reply_text.call_args
        self.assertIn("Help & Commands", args[0])

    def test_status_command(self):
        """Test /status command response"""
        mock_update = Mock()
        mock_message = Mock()
        mock_message.reply_text = AsyncMock()
        mock_update.message = mock_message

        # Run the command
        asyncio.run(self.bot.status_command(mock_update, None))

        # Verify response
        mock_message.reply_text.assert_called_once()
        args, kwargs = mock_message.reply_text.call_args
        self.assertIn("Bot Status Dashboard", args[0])

    @patch("bot.asyncio.create_task")
    def test_handle_voice(self, mock_create_task):
        """Test voice message handling"""
        mock_update = Mock()
        mock_message = Mock()
        mock_message.voice = Mock()
        mock_update.message = mock_message

        # Run the handler
        asyncio.run(self.bot.handle_voice(mock_update, None))

        # Verify task creation
        mock_create_task.assert_called_once()


if __name__ == "__main__":
    unittest.main()
