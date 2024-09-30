# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-lunarbase
"""Component that convert htmls to texts
inputs:
  Scraper_results (dict): e.g {'https://example.com': {'content': '<html><body>Hello World</body></html>'}}
Output (dict): The converted htmls in texts e.g {'https://example.com': {'text': 'Hello World', 'content': '<html><body>Hello World</body></html>'}}
"""

from typing import Any, Dict, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from bs4 import BeautifulSoup


def htmls_to_texts(scraper_results: Dict[str, Dict[str, str]]):
    """
    Processes HTML content from scraper results to extract plain text, keeping the original HTML.

    This function takes the output of a web scraping process, which includes URLs with their
    corresponding HTML content or errors. It parses each HTML content to extract plain text,
    adding this plain text to the results under a new "text" key, while retaining the original
    HTML content under the "content" key. If an error was encountered for a specific URL
    (indicated by an "error" key), the entry is left unchanged, preserving the error message.

    Parameters:
    - scraper_results (Dict[str, Dict[str, str]]): A dictionary with the results of a web scraping
      process. Each key is a URL, and each value is a dictionary that may contain a "content" key
      with HTML content or an "error" key with an error message.

    Returns:
    - Dict[str, Dict[str, str]]: A dictionary similar to the input, but with each successfully
      processed URL's dictionary containing both the original "content" key with HTML content and
      a new "text" key with the converted plain text. URLs with errors remain unchanged.

    Examples:
    >>> htmls_to_texts({'https://example.com': {'content': '<html><body>Hello World</body></html>'}})
    {'https://example.com': {'text': 'Hello World', 'content': '<html><body>Hello World</body></html>'}}

    >>> htmls_to_texts({'https://example.com': {'error': 'A http error occurred'}})
    {'https://example.com': {'error': 'A http error occurred'}}

    Note:
    - The function utilizes the `BeautifulSoup` library from `bs4` for HTML parsing and text extraction.
    - It ensures that both the raw HTML content and its plain text conversion are available in the output
      for each URL, facilitating further processing or analysis that may require access to both formats.
    """
    results_with_html: Dict[str, Dict[str, str]] = dict()
    for url, result in scraper_results.items():
        my_dict: Dict[str, str] = dict()
        my_dict.update(**result)
        if "error" not in result and "content" in result:
            html_content = result["content"]
            soup = BeautifulSoup(html_content, features="html.parser")
            my_dict["text"] = soup.get_text()
        results_with_html[url] = my_dict
    return results_with_html


class HTMLsToTexts(
    BaseComponent,
    component_name="Htmls2Texts",
    component_description="""Converts HTMLs to texts.
Inputs:
  `scraper_results` (Dict[str, Dict[str, str]]): A dictionary with the URLs as keys, mapped to a dictionary with a key `content` mapped to their HTMLs if the HTMLs were scraped succesfully. E.g. `{`https://example.com`: {`content`: `<html><body>Hello World</body></html>`}}`.
Output ([str, Dict[str, str]]): A dictionary similar to the input, but with an additional key `text` in each URL dictionary, mapped to the extracted from the HTML. URLs with errors remain unchanged. E.g. `{`https://example.com`: {`text`: `Hello World`, `content`: `<html><body>Hello World</body></html>`}}`""",
    input_types={"scraper_results": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def __init__(
        self,
        model: Optional[ComponentModel] = None,
        **kwargs: Any,
    ):
        super().__init__(model=model, configuration=kwargs)

    def run(self, scraper_results: Dict) -> Dict[str, Dict[str, str]]:
        return htmls_to_texts(scraper_results)
