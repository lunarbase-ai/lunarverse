# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-lunarbase
"""Component to scrape URLs sequantially
Inputs:
  Urls (List[Dict[str, Any] | str]]): List of the URLs. Two possible format:
    List of url directly
    List of dict which contains "URL" as key and the url as the value.
Output (Dict[str, Dict[str, str]]): for each url, either the content e.g {'https://example.com': {'content': '...'}} or an error e.g {'https://invalidurl.com': {'error': 'Invalid URL: ...'}}
"""

from typing import Any, Dict, List, Optional

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
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


def scrape_urls(urls: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Scrape content from a list of URLs and return their content or errors encountered.

    For each URL, this function attempts to make a GET request. If the request is successful
    (HTTP status code is less than 400), it stores the response content. Otherwise, it records
    the specific error encountered during the request. This includes handling for common issues
    such as timeouts, too many redirects, invalid URLs, decoding errors, SSL errors, and other
    general request exceptions.

    Parameters:
    - urls (List[str]): A list of strings, where each string is a URL to be scraped.

    Returns:
    - Dict[str, Dict[str, str]]: A dictionary where each key is a URL from the input list.
      The value for each key is another dictionary with either a "content" key containing
      the scraped content as a string (if the request was successful), or an "error" key
      with a descriptive error message (if the request failed).

    Examples:
    >>> scrape_urls(['https://example.com'])
    {'https://example.com': {'content': '...'}}

    >>> scrape_urls(['https://invalidurl.com'])
    {'https://invalidurl.com': {'error': 'Invalid URL: ...'}}

    Note:
    - The function depends on the `requests` library for making HTTP requests.
    - Errors are caught and recorded individually for each URL, allowing the function
      to proceed with subsequent URLs even if one fails.
    """
    results: Dict[str, Dict[str, str]] = dict()
    for url in urls:
        try:
            r = requests.get(url)
            if r.status_code < 400:
                results[url] = {"content": r.content.decode("utf-8")}
            else:
                results[url] = {"error": f"A http error {r.status_code} occured"}
        except Timeout as e:
            results[url] = {"error": f"A timeout occurred: {e}"}
        except TooManyRedirects as e:
            results[url] = {"error": f"Too many redirects: {e}"}
        except URLRequired as e:
            results[url] = {"error": f"A valid URL is required: {e}"}
        except InvalidURL as e:
            results[url] = {"error": f"Invalid URL: {e}"}
        except ContentDecodingError as e:
            results[url] = {"error": f"Error decoding response content: {e}"}
        except RetryError as e:
            results[url] = {"error": f"Request failed after retries: {e}"}
        except SSLError as e:
            results[url] = {"error": f"SSL error: {e}"}
        except RequestException as e:
            results[url] = {"error": f"An exception occurred during the request: {e}"}
        except Exception as e:
            results[url] = {"error": f"An unexpected exception occurred: {e}"}

    return results


class URLsScraper(
    BaseComponent,
    component_name="URLs Scraper",
    component_description="""Scrapes URLs.
Inputs:
  `Urls` (List[str]): A list of URLs (strings) that are to be scraped
Output (Dict[str, Dict[str, str]]): A dictionary where each key is a URL from the input list. The value for each key is another dictionary with either a key `content` (str) containing the scraped content as a string (if the request was successful), or a key `error` with a descriptive error message (if the request failed).""",
    input_types={"urls": DataType.LIST},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def __init__(
        self,
        model: Optional[ComponentModel] = None,
        **kwargs: Any,
    ):
        super().__init__(model=model, configuration=kwargs)

    def run(self, urls: List[str]):
        if urls and isinstance(urls[0], dict):
            urls = [a["URL"] for a in urls]
        return scrape_urls(urls)
