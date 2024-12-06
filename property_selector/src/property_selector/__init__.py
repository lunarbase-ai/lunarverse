# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Dict

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from property_selector.utils import get_nested_value_from_dict


class PropertySelector(
    LunarComponent,
    component_name="Property Selector",
    component_description="""Get values of properties (keys) of an inputted dictionary.
Inputs:
  `data` (Dict[str, Any]): A dictionary to extract values from. E.g. `{`keyA`: {`keyB`: 123}, `keyC`: {`keyD`: 456}}`
  `Selected properties` (str): A comma separated string of the properties (keys) to extract, using dots for nested properties. E.g. `keyA,keyC.keyD`
Output (Dict): A dictionary of the selected properties and their values. E.g. `{`keyA`: {`keyB`: 123}, `keyC.keyD`: 456}`""",
    input_types={
        "inputs": DataType.AGGREGATED,
        "selected_properties": DataType.PROPERTY_SELECTOR,
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_TRANSFORMATION,
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)

    def run(
        self,
        data: Dict,
        selected_properties: str,
    ):
        if not selected_properties:
            return {}

        selected_properties_list = [prop.strip() for prop in selected_properties.split(',')]
        result = {}

        for prop in selected_properties_list:
            keys = prop.split('.')
            try:
                result[prop] = get_nested_value_from_dict(data, keys)
            except KeyError:
                result[prop] = None

        return result
