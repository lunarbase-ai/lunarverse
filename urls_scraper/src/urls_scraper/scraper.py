from typing import Dict, List, Optional
from pydantic import BaseModel, HttpUrl

import requests
from requests.exceptions import (
    Timeout,
    TooManyRedirects,
    URLRequired,
    InvalidURL,
    ContentDecodingError,
    RetryError,
    SSLError,
    RequestException,
)


class ScraperResultModel(BaseModel):
    success: bool
    content: str
    code: int = 0
    error: Optional[str] = None


def scrape_urls(urls: List[HttpUrl]) -> Dict[HttpUrl, ScraperResultModel]:
    results: Dict[HttpUrl, ScraperResultModel] = dict()
    for url in urls:
        try:
            r = requests.get(url)
            if r.status_code < 400:
                results[url] = ScraperResultModel(
                    success=True,
                    content=r.content.decode("utf-8"),
                    code=r.status_code
                ).model_dump(exclude_none=True)
            else:
                results[url] = ScraperResultModel(
                    success=False,
                    content="",
                    code=r.status_code,
                    error=f"A http error {r.status_code} occurred"
                ).model_dump(exclude_none=True)
        except Timeout as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"A timeout occurred: {e}"
            ).model_dump(exclude_none=True)
        except TooManyRedirects as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"Too many redirects: {e}"
            ).model_dump(exclude_none=True)
        except URLRequired as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"A valid URL is required: {e}"
            ).model_dump(exclude_none=True)
        except InvalidURL as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"Invalid URL: {e}"
            ).model_dump(exclude_none=True)
        except ContentDecodingError as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"Error decoding response content: {e}"
            ).model_dump(exclude_none=True)
        except RetryError as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"Request failed after retries: {e}"
            ).model_dump(exclude_none=True)
        except SSLError as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"SSL error occurred: {e}"
            ).model_dump(exclude_none=True)
        except RequestException as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"A request exception occurred: {e}"
            ).model_dump(exclude_none=True)
        except Exception as e:
            results[url] = ScraperResultModel(
                success=False,
                content="",
                error=f"An unexpected exception occurred: {e}"
            ).model_dump(exclude_none=True)

    return results