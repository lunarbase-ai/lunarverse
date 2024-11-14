import pytest
from property_getter import PropertyGetter



class TestPropertyGetter:

    @pytest.fixture
    def component(self):
        return PropertyGetter()

    def test_simple_dictionary(self, component):
        input_data = {
            "name": "Alice",
            "age": 25,
            "city": "Los Angeles"
        }
        selected_property = "name"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == "Alice"

    def test_nested_dictionaries(self, component):
        input_data = {
            "user": {
                "name": "Bob",
                "details": {
                    "age": 28,
                    "city": "Chicago"
                }
            }
        }
        selected_property = "user.details.city"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == "Chicago"

    def test_list_of_dictionaries(self, component):
        input_data = [
            {"id": 1, "name": "Charlie"},
            {"id": 2, "name": "Diana"}
        ]
        selected_property = "1.name"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == "Diana"

    def test_list_of_strings(self, component):
        input_data = [
            'Banana',
            'Apple',
            'Orange'
        ]
        selected_property = "1"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == "Apple"

    def test_list_of_dictionaries_with_nested_dictionaries(self, component):
        input_data = [
            {
                "id": 1,
                "name": "Alice",
                "details": {
                    "age": 25,
                    "city": "Los Angeles"
                },
                "pet_names": ["Fluffy", "Spot"]
            },
            {
                "id": 2,
                "name": "Bob",
                "details": {
                    "age": 28,
                    "city": "Chicago"
                },
                "pet_names": ["Rex", "Max"]
            }
        ]
        selected_property = "1.pet_names.0"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == "Rex"

    def test_invalid_property(self, component):
        input_data = {
            "name": "Alice",
            "age": 25,
            "city": "Los Angeles"
        }
        selected_property = "invalid_property"
        with pytest.raises(ValueError):
            component.run(input=input_data, selected_property=selected_property)

    def test_invalid_nested_property(self, component):
        input_data = {
            "user": {
                "name": "Bob",
                "details": {
                    "age": 28,
                    "city": "Chicago"
                }
            }
        }
        selected_property = "user.invalid_property"
        with pytest.raises(ValueError):
            component.run(input=input_data, selected_property=selected_property)

    def test_invalid_list_index(self, component):
        input_data = [
            'Banana',
            'Apple',
            'Orange'
        ]
        selected_property = "5"
        with pytest.raises(ValueError):
            component.run(input=input_data, selected_property=selected_property)

    def test_invalid_list_index_in_dict(self, component):
        input_data = [
            {"id": 1, "name": "Charlie"},
            {"id": 2, "name": "Diana"}
        ]
        selected_property = "5.name"
        with pytest.raises(ValueError):
            component.run(input=input_data, selected_property=selected_property)