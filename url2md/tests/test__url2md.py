import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import os
from url2md import URL2MD

class TestUrl2Md:
    def setup_method(self):
        self.test_url = "https://www.example.com/test-page"
        self.test_output_dir = "test_files"
        self.mock_result = MagicMock(markdown="# Mock Markdown Content")
        self.component = URL2MD()

    def teardown_method(self):
        if os.path.exists(self.test_output_dir):
            for file in os.listdir(self.test_output_dir):
                os.remove(os.path.join(self.test_output_dir, file))
            os.rmdir(self.test_output_dir)

    @patch('url2md.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2md_successful_conversion(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = self.mock_result

        result = await self.component.run(self.test_url)

        assert result is not None and os.path.exists(result) and result.endswith('.md')

    @patch('url2md.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2md_no_markdown_content(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = MagicMock(markdown=None)

        result = await self.component.run(self.test_url)

        assert result is None

    @patch('url2md.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2md_special_characters_in_url(self, mock_crawler_class):
        special_url = "https://www.example.com/test-page!@#$%^&*()"
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = self.mock_result

        result = await self.component.run(special_url)

        assert all(not char in result for char in "!@#$%^&*()")

    @patch('url2md.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2md_empty_path(self, mock_crawler_class):
        empty_path_url = "https://www.example.com"
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = self.mock_result

        result = await self.component.run(empty_path_url)

        assert "page.md" in result
