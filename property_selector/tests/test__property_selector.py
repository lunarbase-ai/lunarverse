import pytest
from property_selector import PropertySelector

# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later


class TestPropertySelector:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.property_selector = PropertySelector()

    def test_valid_nested_properties(self):
        data = {
            "keyA": {"keyB": 123},
            "keyC": {"keyD": 456}
        }
        selected_properties = "keyA,keyC.keyD"
        expected_output = {
            "keyA": {"keyB": 123},
            "keyC.keyD": 456
        }
        result = self.property_selector.run(data, selected_properties)
        assert result == expected_output

    def test_non_existent_properties(self):
        data = {
            "keyA": {"keyB": 123},
            "keyC": {"keyD": 456}
        }
        selected_properties = "keyX,keyC.keyY"
        expected_output = {
            "keyX": None,
            "keyC.keyY": None
        }
        result = self.property_selector.run(data, selected_properties)
        assert result == expected_output

    def test_mix_of_valid_and_non_existent_properties(self):
        data = {
            "keyA": {"keyB": 123},
            "keyC": {"keyD": 456}
        }
        selected_properties = "keyA,keyC.keyD,keyX"
        expected_output = {
            "keyA": {"keyB": 123},
            "keyC.keyD": 456,
            "keyX": None
        }
        result = self.property_selector.run(data, selected_properties)
        assert result == expected_output

    def test_empty_properties_string(self):
        data = {
            "keyA": {"keyB": 123},
            "keyC": {"keyD": 456}
        }
        selected_properties = ""
        expected_output = {}
        result = self.property_selector.run(data, selected_properties)
        assert result == expected_output