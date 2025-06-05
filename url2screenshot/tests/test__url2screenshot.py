# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import os
import base64
from url2screenshot import URL2Screenshot


class TestURL2Screenshot:
    def setup_method(self):
        self.test_url = "https://www.example.com/test-page"
        self.test_output_dir = "test_files"
        mock_screenshot_bytes = b"mock screenshot content"
        self.mock_screenshot_base64 = base64.b64encode(mock_screenshot_bytes).decode('utf-8')
        self.mock_result = MagicMock(screenshot=self.mock_screenshot_base64)
        self.component = URL2Screenshot()

    def teardown_method(self):
        if os.path.exists(self.test_output_dir):
            for file in os.listdir(self.test_output_dir):
                os.remove(os.path.join(self.test_output_dir, file))
            os.rmdir(self.test_output_dir)

    @patch('url2screenshot.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2screenshot_successful_capture(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = self.mock_result

        result = await self.component.run(self.test_url)

        assert result is not None
        assert os.path.exists(result)
        assert result.endswith('.jpg')

    @patch('url2screenshot.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2screenshot_no_screenshot_content(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = MagicMock(screenshot=None)

        result = await self.component.run(self.test_url)

        assert result is None

    @patch('url2screenshot.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2screenshot_special_characters_in_url(self, mock_crawler_class):
        special_url = "https://www.example.com/test-page!@#$%^&*()"
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = self.mock_result

        result = await self.component.run(special_url)

        assert result is not None
        assert all(not char in result for char in "!@#$%^&*()")

    @patch('url2screenshot.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2screenshot_empty_path(self, mock_crawler_class):
        empty_path_url = "https://www.example.com"
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = self.mock_result

        result = await self.component.run(empty_path_url)

        assert result is not None
        assert "index.jpg" in result
