import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import cleanup_temp_file, format_transcription, format_processing_time, get_file_info


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

        # Test with processing time
        text_with_time = "Hello world"
        formatted_with_time = format_transcription(text_with_time, 1.25)
        self.assertIn("📝 *Transcription:*", formatted_with_time)
        self.assertIn("Hello world.", formatted_with_time)
        self.assertIn("⏱️ *Processing time:*", formatted_with_time)
        self.assertIn("1.2s", formatted_with_time)

    def test_format_processing_time(self):
        """Test processing time formatting"""
        # Test sub-second time
        formatted_sub = format_processing_time(0.85)
        self.assertIn("⏱️ *Processing time:*", formatted_sub)
        self.assertIn("0.85s", formatted_sub)

        # Test seconds
        formatted_sec = format_processing_time(5.7)
        self.assertIn("⏱️ *Processing time:*", formatted_sec)
        self.assertIn("5.7s", formatted_sec)

        # Test minutes and seconds
        formatted_min = format_processing_time(75.3)
        self.assertIn("⏱️ *Processing time:*", formatted_min)
        self.assertIn("1m 15.3s", formatted_min)

        # Test exact minute
        formatted_exact = format_processing_time(120.0)
        self.assertIn("⏱️ *Processing time:*", formatted_exact)
        self.assertIn("2m 0.0s", formatted_exact)

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
