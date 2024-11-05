# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-lunarbase
"""Component that convert htmls to texts
inputs:
  html_content_mapper (dict): e.g {'https://example.com': {'content': '<html><body>Hello World</body></html>'}}
Output (dict): The converted htmls in texts e.g {'https://example.com': {'text': 'Hello World', 'content': '<html><body>Hello World</body></html>'}}
"""

from typing import Any

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from html2text.extractor import HTMLTextExtractor, HTMLContentMapperModel

class HTML2Text(
    LunarComponent,
    component_name="Htmls2Texts",
    component_description="""Converts HTMLs to texts.
    Inputs:
    `html_content_mapper` (Dict[str, Dict[str, str]]): A dictionary with the URLs as keys, mapped to a dictionary with a key `content` mapped to their HTMLs. E.g. `{`https://example.com`: {`content`: `<html><body>Hello World</body></html>`}}`.
    Output ([str, Dict[str, str]]): A dictionary similar to the input, but with an additional key `text` in each URL dictionary, mapped to the extracted from the HTML. E.g. `{`https://example.com`: {`text`: `Hello World`, `content`: `<html><body>Hello World</body></html>`}}`""",
    input_types={"html_content_mapper": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def __init__(self, **kwargs: Any,):
        super().__init__(configuration=kwargs)
        self.extractor = HTMLTextExtractor()

    def run(self, html_content_mapper: HTMLContentMapperModel) -> HTMLContentMapperModel:
        return self.extractor.extract(html_content_mapper)
