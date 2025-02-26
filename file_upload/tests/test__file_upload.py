from lunarcore.component.data_types import File
from file_upload.src.file_upload import FileUpload


class TestFileUpload:

    def setup_method(self):
        self.component = FileUpload()

    def test_run_success(self):
        mock_file = File(path="/mock/path/to/file.txt")
        result = self.component.run(mock_file)
        assert result == "/mock/path/to/file.txt"
