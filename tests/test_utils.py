import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import cleanup_temp_file, format_transcription, get_file_info


class TestUtils(unittest.TestCase):
    def test_format_transcription(self):
        """Test transcription formatting"""
        # Test normal text
        text = "Hello world"
        formatted = format_transcription(text)
        self.assertIn("📝 *Transcription:*", formatted)
        self.assertIn("Hello world.", formatted)

        # Test empty text
        empty_text = ""
        formatted_empty = format_transcription(empty_text)
        self.assertIn("No speech detected", formatted_empty)

        # Test text already ending with period
        text_with_period = "Hello world."
        formatted_period = format_transcription(text_with_period)
        self.assertIn("Hello world.", formatted_period)
        # Should not add double period
        self.assertNotIn("Hello world..", formatted_period)

    def test_get_file_info(self):
        """Test file info extraction"""
        # Mock file object
        mock_file = Mock()
        mock_file.file_size = 1024000  # 1MB
        mock_file.file_id = "test_file_id"

        # Test with all attributes
        info = get_file_info(mock_file)
        self.assertIsInstance(info, str)
        self.assertIn("test_file_id", info)
        self.assertIn("0.98MB", info)  # 1024000 bytes = 0.98MB

        # Test with no file_size
        mock_file.file_size = None
        info_no_size = get_file_info(mock_file)
        self.assertIsInstance(info_no_size, str)
        self.assertIn("0.00MB", info_no_size)

    @patch("utils.os.path.exists")
    @patch("utils.os.unlink")
    def test_cleanup_temp_file(self, mock_unlink, mock_exists):
        """Test temporary file cleanup"""
        # Test file exists
        mock_exists.return_value = True
        cleanup_temp_file("/tmp/test.mp3")
        mock_unlink.assert_called_once_with("/tmp/test.mp3")

        # Test file doesn't exist
        mock_exists.return_value = False
        mock_unlink.reset_mock()
        cleanup_temp_file("/tmp/nonexistent.mp3")
        mock_unlink.assert_not_called()

        # Test with exception
        mock_exists.return_value = True
        mock_unlink.side_effect = OSError("Permission denied")
        # Should not raise exception
        cleanup_temp_file("/tmp/test.mp3")


if __name__ == "__main__":
    unittest.main()
