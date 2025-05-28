import pytest
from deep_crawling import DeepCrawling

@pytest.mark.asyncio
async def test_deep_crawling_basic():
    component = DeepCrawling()
    result = await component.run(
        url="https://example.com",
        instruction="Extract the main heading",
        include_external=False,
        max_depth=1
    )
    assert result is not None
    assert "url" in result
    assert "extracted_content" in result
    assert "visited_urls" in result
    assert "depth" in result

@pytest.mark.asyncio
async def test_deep_crawling_with_external():
    component = DeepCrawling()
    result = await component.run(
        url="https://example.com",
        instruction="Extract all headings",
        include_external=True,
        max_depth=2
    )
    assert result is not None
    assert len(result["visited_urls"]) > 1

@pytest.mark.asyncio
async def test_deep_crawling_invalid_url():
    component = DeepCrawling()
    result = await component.run(
        url="https://invalid-url-that-does-not-exist.com",
        instruction="Extract anything",
        include_external=False,
        max_depth=1
    )
    assert result is None

@pytest.mark.asyncio
async def test_deep_crawling_max_depth():
    component = DeepCrawling()
    max_depth = 3
    result = await component.run(
        url="https://example.com",
        instruction="Extract all links",
        include_external=True,
        max_depth=max_depth
    )
    assert result is not None
    assert result["depth"] <= max_depth 