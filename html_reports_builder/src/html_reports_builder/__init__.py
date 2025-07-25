# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-lunarbase
"""Component to generate html report based on jinja2 (in batch)
inputs:
  Template_j2 (str):Jinja2 template e.g "<html><head><title>{{ title }}</title></head></html>"
  Data (dict): data to render the templates e.g {"william": {"title": "William is cool"}}
Output (dict): The rendered templates e.g {"william": "<html><head><title>William is cool</title></head></html>"}
"""

from typing import Any, Dict, List, Optional

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from jinja2 import Template
from markupsafe import escape


class HTMLReportsBuilder(
    LunarComponent,
    component_name="HTML Reports Builder",
    component_description="""Converts HTML content into a downloadable document, such as a PDF, preserving the layout and styling.
Inputs:
  `Template_j2` (str): A Jinja2 template of the HTML report template as a string, e.g. `<html><head><title>{{ title }}</title></head></html>`
  `Data` (Dict[str, Dict[str, str]]): A dictionary with labels (strings) as keys, where each label is mapped to a dictionary for rendering the template. In this sub-dictionaru, each key-value pair is a template_variable and the template_variable value in the Jinja2 template, e.g {`william`: {`title`: `William is cool`}}
Output (Dict[str, str]): A dictionary where each inputted label is mapped to the corresponding rendered template, e.g {`william`: `<html><head><title>William is cool</title></head></html>`}""",
    input_types={"template_j2": DataType.TEXT, "data": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.UTILS,
):
    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(configuration=kwargs)

    def run(self, template_j2: str, data: Dict) -> Dict[str, str]:
        template_j2 = Template(template_j2)
        results: Dict[str, str] = dict()
        for key, sub_dict in data.items():
            # Convert None values to empty strings and escape special characters
            sanitized_sub_dict = {k: escape(v if v is not None else "") for k, v in sub_dict.items()}
            results[key] = template_j2.render(**sanitized_sub_dict)
        return results