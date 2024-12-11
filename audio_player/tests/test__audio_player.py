import pytest
from audio_player import AudioPlayer

class TestAudioPlayer:
    def setup_method(self):
        self.audio_player = AudioPlayer()

    def test_valid_wav_audio(self):
        valid_audio_data = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAABCxAgAEABAAZGF0YQAAAAA="
        result = self.audio_player.run(valid_audio_data)
        assert result == valid_audio_data

    def test_valid_mp3_audio(self):
        valid_mp3_audio_data = "data:audio/mp3;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjQxLjEwMAAAAAAAAAAAAAAA//tQxA=="
        result = self.audio_player.run(valid_mp3_audio_data)
        assert result == valid_mp3_audio_data

    def test_valid_mpeg_audio(self):
        valid_mpeg_audio_data = "data:audio/mpeg;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjQxLjEwMAAAAAAAAAAAAAAA//tQxA=="
        result = self.audio_player.run(valid_mpeg_audio_data)
        assert result == valid_mpeg_audio_data

    def test_empty_audio_data(self):
        empty_audio_data = ""
        with pytest.raises(ValueError, match="Empty audio data"):
            self.audio_player.run(empty_audio_data)

    def test_non_base64_audio_data(self):
        non_base64_audio_data = "data:audio/wav;base64,12345"
        with pytest.raises(ValueError, match="Invalid Base64 encoded audio"):
            self.audio_player.run(non_base64_audio_data)

    def test_base64_audio_with_missing_padding(self):
        audio_data_with_missing_padding = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAABCxAgAEABAAZGF0YQAAAA"
        expected_result = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAABCxAgAEABAAZGF0YQAAAA=="
        result = self.audio_player.run(audio_data_with_missing_padding)
        assert result == expected_result

    def test_missing_mime_type(self):
        missing_mime_type_audio_data = "data:;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAABCxAgAEABAAZGF0YQAAAAA="
        with pytest.raises(ValueError, match="Invalid MIME type"):
            self.audio_player.run(missing_mime_type_audio_data)