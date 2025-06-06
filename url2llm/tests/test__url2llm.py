# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from url2llm import URL2LLM

class TestUrl2LLM:
    def setup_method(self):
        self.test_url = "https://www.example.com/test-page"
        self.test_prompt = "Extract main information from this page"
        self.mock_result = MagicMock(extracted_content="Content extracted by LLM")
        self.component = URL2LLM(
            provider="azure",
            base_url="https://test.openai.azure.com/",
            api_key_token="test-key"
        )

    @patch('url2llm.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2llm_successful_extraction(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = self.mock_result

        result = await self.component.run(self.test_url, self.test_prompt)

        assert result is not None
        assert isinstance(result, dict)
        assert "url" in result
        assert "extracted_content" in result
        assert result["url"] == self.test_url
        assert result["extracted_content"] == "Content extracted by LLM"

    @patch('url2llm.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2llm_no_extracted_content(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.return_value = MagicMock(extracted_content=None)

        result = await self.component.run(self.test_url, self.test_prompt)

        assert result is None

    @patch('url2llm.AsyncWebCrawler')
    @pytest.mark.asyncio
    async def test_url2llm_invalid_url(self, mock_crawler_class):
        mock_crawler_instance = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler_instance
        mock_crawler_instance.arun.side_effect = Exception("Invalid URL")

        with pytest.raises(Exception) as exc_info:
            await self.component.run("https://invalid-url.com", self.test_prompt)
        
        assert str(exc_info.value) == "Invalid URL" 