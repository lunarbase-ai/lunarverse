import pytest
from unittest.mock import patch, AsyncMock
from pubmed_searcher.pubmed_scraper import get_num_pages, build_article_urls, get_article_data, extract_by_article
from pydantic import BaseModel

class ArticleDetails(BaseModel):
    abstract: str
    affiliations: list
    keywords: str
    title: str
    authors: str
    journal: str

class TestAsyncPubmedScraper:

    @patch('pubmed_searcher.pubmed_scraper.requests.get')
    def test_get_num_pages(self, mock_get):
        mock_response = mock_get.return_value.__enter__.return_value
        mock_response.text = '<span class="total-pages">10</span>'
        
        num_pages = get_num_pages('cancer', None, 'https://pubmed.ncbi.nlm.nih.gov')
        assert num_pages == 10

    @pytest.mark.asyncio
    @patch('pubmed_searcher.pubmed_scraper.get_pmids')
    async def test_build_article_urls(self, mock_get_pmids):
        mock_get_pmids.return_value = AsyncMock()
        
        await build_article_urls(['cancer'], 2, 0, 1, 'https://pubmed.ncbi.nlm.nih.gov')
        assert mock_get_pmids.call_count == 2

    @pytest.mark.asyncio
    @patch('pubmed_searcher.pubmed_scraper.extract_by_article')
    async def test_get_article_data(self, mock_extract):
        mock_extract.return_value = AsyncMock()
        urls = ['https://pubmed.ncbi.nlm.nih.gov/12345678/']
        
        await get_article_data(urls)
        mock_extract.assert_called_with('https://pubmed.ncbi.nlm.nih.gov/12345678/')

    @pytest.mark.asyncio
    @patch('pubmed_searcher.pubmed_scraper.aiohttp.ClientSession.get')
    async def test_extract_article_details(self, mock_get):
        mock_response = AsyncMock()
        mock_response.text.return_value = """
        <div class="abstract-content selected">
            <p>Abstract paragraph one.</p>
            <p>Abstract paragraph two.</p>
        </div>
        <ul class="item-list">
            <li>Affiliation One</li>
            <li>Affiliation Two</li>
        </ul>
        <strong class="sub-title">Keywords:</strong>
        <div class="abstract">
            <p>keyword1, keyword2</p>
        </div>
        <meta name="citation_title" content="Sample Title" />
        <div class="authors-list">
            <a class="full-name">Author One</a>
            <a class="full-name">Author Two</a>
        </div>
        <meta name="citation_journal_title" content="Sample Journal" />
        """
        mock_get.return_value.__aenter__.return_value = mock_response

        url = 'https://pubmed.ncbi.nlm.nih.gov/12345678/'
        details = await extract_by_article(url)

        expected = {
            "url": 'https://pubmed.ncbi.nlm.nih.gov/12345678/',
            "abstract": 'Abstract paragraph one. Abstract paragraph two.',
            "affiliations": ['Affiliation One', 'Affiliation Two'],
            "keywords": 'keyword1, keyword2',
            "title": 'Sample Title',
            "authors": 'Author One, Author Two, ',
            "journal": 'Sample Journal',
            "date": 'NO_DATE'
        }

        assert details == expected