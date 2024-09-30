# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Any, Optional, List, Dict
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from lunarcore.utils import select_property_from_dict


class PropertySelector(
    BaseComponent,
    component_name="Property Selector",
    component_description="""Get values of properties (keys) of an inputted dictionary.
Inputs:
  `Inputs` (Dict[str, Any]): A dictionary to extract values from. E.g. `{`keyA`: {`keyB`: 123}, `keyC`: {`keyD`: 456}}`
  `Selected properties` (str): A comma separated string of the properties (keys) to extract, using dots for nested properties. E.g. `keyA,keyC.keyD`
Output (Dict): A dictionary of the selected properties and their values. E.g. `{`keyA`: {`keyB`: 123}, `keyC.keyD`: 456}`""",
    input_types={
        "inputs": DataType.AGGREGATED,
        "selected_properties": DataType.PROPERTY_SELECTOR,
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_TRANSFORMATION,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

    def run(
        self,
        inputs: Dict,
        selected_properties: str,
    ):
        selected_properties_keys = selected_properties.split(",")
        selected_properties_values = {}
        for selected_properties_key in selected_properties_keys:
            selected_properties_values[
                selected_properties_key
            ] = select_property_from_dict(inputs, selected_properties_key)

        return selected_properties_values
