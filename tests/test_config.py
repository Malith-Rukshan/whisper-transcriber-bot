import os
import sys
import unittest
from unittest.mock import patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Store original values
        self.original_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.original_model_path = os.environ.get("WHISPER_MODEL_PATH")

    def tearDown(self):
        """Clean up after tests"""
        # Restore original values
        if self.original_token:
            os.environ["TELEGRAM_BOT_TOKEN"] = self.original_token
        elif "TELEGRAM_BOT_TOKEN" in os.environ:
            del os.environ["TELEGRAM_BOT_TOKEN"]

        if self.original_model_path:
            os.environ["WHISPER_MODEL_PATH"] = self.original_model_path
        elif "WHISPER_MODEL_PATH" in os.environ:
            del os.environ["WHISPER_MODEL_PATH"]

    def test_config_defaults(self):
        """Test config default values"""
        self.assertEqual(Config.BOT_USERNAME, "TranscriberXBOT")
        self.assertEqual(Config.WHISPER_MODEL_NAME, "base.en")
        self.assertEqual(Config.MAX_AUDIO_SIZE_MB, 50)
        self.assertEqual(Config.LOG_LEVEL, "INFO")
        self.assertIn("mp3", Config.SUPPORTED_FORMATS)
        self.assertIn("wav", Config.SUPPORTED_FORMATS)

    def test_config_validation_success(self):
        """Test successful config validation"""
        # Set required environment variables
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"

        # Mock model file existence
        with patch("config.os.path.exists") as mock_exists:
            mock_exists.return_value = True

            # Should not raise exception
            Config.validate()

    def test_config_validation_no_token(self):
        """Test config validation without token"""
        # Mock model file existence to isolate token validation
        with patch("config.os.path.exists") as mock_exists:
            mock_exists.return_value = True

            # Mock the token to be None
            with patch.object(Config, "TELEGRAM_BOT_TOKEN", None):
                # Should raise ValueError
                with self.assertRaises(ValueError) as context:
                    Config.validate()
                self.assertIn("TELEGRAM_BOT_TOKEN is required", str(context.exception))

    def test_config_validation_no_model(self):
        """Test config validation without model file"""
        # Set token but no model
        os.environ["TELEGRAM_BOT_TOKEN"] = "test_token"

        # Mock model file not existing
        with patch("config.os.path.exists") as mock_exists:
            mock_exists.return_value = False

            # Should raise ValueError
            with self.assertRaises(ValueError) as context:
                Config.validate()
            self.assertIn("model file not found", str(context.exception))

    def test_environment_variable_override(self):
        """Test environment variable overrides"""
        # Override environment variables
        os.environ["BOT_USERNAME"] = "TestBot"
        os.environ["MAX_AUDIO_SIZE_MB"] = "100"
        os.environ["LOG_LEVEL"] = "DEBUG"

        # Reload module to pick up changes
        import importlib
        import config

        importlib.reload(config)

        # Check overrides
        self.assertEqual(config.Config.LOG_LEVEL, "DEBUG")


if __name__ == "__main__":
    unittest.main()
