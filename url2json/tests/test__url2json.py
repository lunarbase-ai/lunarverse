# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from url2json import URL2JSON

class TestUrl2Json:
    def setup_method(self):
        self.test_url = "https://www.example.com/test-page"
        self.mock_result = MagicMock(html="<html>Mock HTML Content</html>")
        self.component = URL2JSON()

    @patch('url2json.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2json_successful_conversion(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = self.mock_result

        result = await self.component.run(self.test_url)

        assert result is not None
        assert isinstance(result, dict)
        assert "url" in result
        assert "html_content" in result
        assert result["url"] == self.test_url
        assert "<html" in result["html_content"].lower()

    @patch('url2json.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2json_no_html_content(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = MagicMock(html=None)

        result = await self.component.run(self.test_url)

        assert result is None

    @patch('url2json.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2json_invalid_url(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.side_effect = Exception("Invalid URL")

        result = await self.component.run("https://invalid-url.com")

        assert result is None 