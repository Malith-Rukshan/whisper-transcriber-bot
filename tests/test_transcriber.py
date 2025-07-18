import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from transcriber import WhisperTranscriber


class TestWhisperTranscriber(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Mock the config and model
        self.config_patcher = patch("transcriber.Config")
        self.mock_config = self.config_patcher.start()
        self.mock_config.WHISPER_MODEL_PATH = "/mock/path/model.bin"

        self.model_patcher = patch("transcriber.Model")
        self.mock_model_class = self.model_patcher.start()
        self.mock_model = Mock()
        self.mock_model.transcribe = Mock()
        self.mock_model_class.return_value = self.mock_model

    def tearDown(self):
        """Clean up after tests"""
        self.config_patcher.stop()
        self.model_patcher.stop()

    @patch("transcriber.os.path.exists")
    def test_transcriber_initialization_success(self, mock_exists):
        """Test successful transcriber initialization"""
        mock_exists.return_value = True

        transcriber = WhisperTranscriber()

        self.assertIsNotNone(transcriber.model)
        self.mock_model_class.assert_called_once()

    @patch("transcriber.os.path.exists")
    def test_transcriber_initialization_no_model(self, mock_exists):
        """Test transcriber initialization without model file"""
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError):
            WhisperTranscriber()

    @patch("transcriber.os.path.exists")
    def test_transcriber_initialization_model_error(self, mock_exists):
        """Test transcriber initialization with model error"""
        mock_exists.return_value = True
        self.mock_model_class.side_effect = Exception("Model loading failed")

        with self.assertRaises(Exception):
            WhisperTranscriber()

    @patch("transcriber.os.path.exists")
    def test_transcribe_audio_success(self, mock_exists):
        """Test successful audio transcription"""
        mock_exists.return_value = True

        # Mock transcription segments
        mock_segment = Mock()
        mock_segment.text = "Hello world"
        self.mock_model.transcribe.return_value = [mock_segment]

        transcriber = WhisperTranscriber()

        # Use asyncio.run for async test
        import asyncio

        result = asyncio.run(transcriber.transcribe_audio("/path/to/audio.wav"))

        # Result should be a tuple (text, processing_time)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Hello world")
        self.assertIsInstance(result[1], float)
        self.assertGreaterEqual(result[1], 0.0)
        self.mock_model.transcribe.assert_called_once_with("/path/to/audio.wav")

    @patch("transcriber.os.path.exists")
    def test_transcribe_audio_empty_result(self, mock_exists):
        """Test transcription with empty result"""
        mock_exists.return_value = True

        # Mock empty transcription
        self.mock_model.transcribe.return_value = []

        transcriber = WhisperTranscriber()

        # Use asyncio.run for async test
        import asyncio

        result = asyncio.run(transcriber.transcribe_audio("/path/to/audio.wav"))

        self.assertIsNone(result)

    @patch("transcriber.os.path.exists")
    def test_transcribe_audio_error(self, mock_exists):
        """Test transcription with error"""
        mock_exists.return_value = True

        # Mock transcription error
        self.mock_model.transcribe.side_effect = Exception("Transcription failed")

        transcriber = WhisperTranscriber()

        # Use asyncio.run for async test
        import asyncio

        result = asyncio.run(transcriber.transcribe_audio("/path/to/audio.wav"))

        self.assertIsNone(result)

    @patch("transcriber.os.path.exists")
    def test_is_healthy(self, mock_exists):
        """Test health check"""
        mock_exists.return_value = True

        transcriber = WhisperTranscriber()
        self.assertTrue(transcriber.is_healthy())

        # Test unhealthy state
        transcriber.model = None
        self.assertFalse(transcriber.is_healthy())


if __name__ == "__main__":
    unittest.main()
