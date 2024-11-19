import pytest
import base64
from unittest.mock import mock_open, patch
from audio2base64 import Audio2Base64

class TestAudio2Base64:

    def setup_method(self):
        self.component = Audio2Base64()
    
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_mp3_data")
    @patch("mimetypes.guess_type", return_value=("audio/mpeg", None))
    def test_run_mp3(self, mock_guess_type, mock_file):
        file_path = "test.mp3"
        expected_data_uri = "data:audio/mpeg;base64," + base64.b64encode(b"fake_mp3_data").decode('utf-8')
        assert self.component.run(file_path) == expected_data_uri

    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_wav_data")
    @patch("mimetypes.guess_type", return_value=("audio/wav", None))
    def test_run_wav(self, mock_guess_type, mock_file):
        file_path = "test.wav"
        expected_data_uri = "data:audio/wav;base64," + base64.b64encode(b"fake_wav_data").decode('utf-8')
        assert self.component.run(file_path) == expected_data_uri

    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_data")
    @patch("mimetypes.guess_type", return_value=(None, None))
    def test_run_invalid_type(self, mock_guess_type, mock_file):
        file_path = "test.txt"
        with pytest.raises(ValueError):
            self.component.run(file_path)

    def test_run_file_not_found(self):
        file_path = "non_existent_file.mp3"
        with pytest.raises(FileNotFoundError):
            self.component.run(file_path)

    def test_run_empty_file_path(self):
        file_path = ""
        with pytest.raises(ValueError):
            self.component.run(file_path)

    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_data")
    def test_run_unsupported_extension(self, mock_file):
        file_path = "test.unsupported"
        with pytest.raises(ValueError):
            self.component.run(file_path)

    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_large_data" * 10000)
    @patch("mimetypes.guess_type", return_value=("audio/mpeg", None))
    def test_run_large_file(self, mock_guess_type, mock_file):
        file_path = "test_large.mp3"
        expected_data_uri = "data:audio/mpeg;base64," + base64.b64encode(b"fake_large_data" * 10000).decode('utf-8')
        assert self.component.run(file_path) == expected_data_uri

    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_mp3_data")
    @patch("mimetypes.guess_type", return_value=("audio/mpeg", None))
    def test_correct_mime_type_detection(self, mock_guess_type, mock_file):
        file_path = "test.mp3"
        assert self.component.run(file_path).startswith("data:audio/mpeg;")