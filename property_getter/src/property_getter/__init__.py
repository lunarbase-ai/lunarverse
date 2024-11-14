# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Union, List, Dict
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class PropertyGetter(
    LunarComponent,
    component_name="Property Getter",
    component_description="""Extracts the mapped value of an inputted key/field/attribute in an inputted object/datastructure. It can be the value of a field/attribute in an object, or the mapped value of a key in a dictionary.
Inputs:
  `Input` (Any): An object to extract a value from. The object can for example be a dictionary, a list, or a File object.
  `Selected property` (str): A string of the name of the key/field/attribute to extract from the inputted object. If needed, the key/field/attribute can be inputted manually by the user. If nested objects/dicts, nested keys can be accessed by concatenating keys with dots (e.g. `parent_dict_key.dict_key`). If, for example, a list of dicts (List[Dict]) is inputted, the list indices are used as keys (e.g. `list_index.dict_key`).
Output (Any): The mapped value of the inputted key/field/attribute in the inputted object.""",
    input_types={"input": DataType.JSON, "selected_property": DataType.PROPERTY_GETTER},
    output_type=DataType.ANY,
    component_group=ComponentGroup.DATA_TRANSFORMATION,
):
    def __init__(self,**kwargs):
        super().__init__(configuration=kwargs)

    @staticmethod
    def get_property_from_dict(dictionary: dict, key_path: str) -> List[Any]:
        parts = key_path.split(".")

        if len(parts) > 1:
            value = dictionary[parts[0]]
            try:
                for p in parts[1:]:
                    if p.strip() == "*":
                        if isinstance(value, dict):
                            return list(value.values())
                        else:
                            return value
                    value = value[p]
            except KeyError:
                raise ValueError(f"The selected property path is invalid: {parts}!")
            return value

        else:
            if key_path == "*":
                return list(dictionary.values())

            try:
                value = dictionary[key_path]
                return value
            except KeyError:
                raise ValueError(
                    f"The selected property <{key_path}> doesn't exist in the input object! Accepted properties: {list(dictionary.keys())}"
                )

    def run(self, input: Union[Dict, List], selected_property: str) -> Any:
        if not isinstance(input, (dict, list)):
            raise ValueError(f"{self.__class__} expects a dict or list input. Got {type(input)}!")

        prop = selected_property.strip()
        parts = prop.split('.')
        value = input

        for p in parts:
            if isinstance(value, list):
                try:
                    index = int(p)
                    value = value[index]
                except (ValueError, IndexError):
                    raise ValueError(f"Invalid list index: {p} in path: {prop}!")
            elif isinstance(value, dict):
                try:
                    value = value[p]
                except KeyError:
                    raise ValueError(f"The selected property path is invalid: {prop}!")
            else:
                raise ValueError(f"Cannot navigate through type: {type(value)}!")

        return value