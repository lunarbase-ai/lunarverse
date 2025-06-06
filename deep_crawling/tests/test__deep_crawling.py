import pytest
from deep_crawling import DeepCrawling

class TestDeepCrawling:
    def setup_method(self):
        self.component = DeepCrawling(
            provider="azure",
            base_url="https://test.openai.azure.com/",
            api_key_token="test-key"
        )
        self.test_url = "https://example.com"
        self.test_instruction = "Extract the main heading"

    @pytest.mark.asyncio
    async def test_deep_crawling_basic(self):
        result = await self.component.run(
            url=self.test_url,
            instruction=self.test_instruction,
            include_external=False,
            max_depth=1
        )
        assert result is not None
        assert "url" in result
        assert "extracted_content" in result
        assert result["url"] == self.test_url

    @pytest.mark.asyncio
    async def test_deep_crawling_with_external(self):
        result = await self.component.run(
            url=self.test_url,
            instruction="Extract all headings",
            include_external=True,
            max_depth=2
        )
        assert result is not None
        assert "url" in result
        assert "extracted_content" in result
        assert result["url"] == self.test_url

    @pytest.mark.asyncio
    async def test_deep_crawling_invalid_url(self):
        result = await self.component.run(
            url="https://invalid-url-that-does-not-exist.com",
            instruction="Extract anything",
            include_external=False,
            max_depth=1
        )
        assert result is None
