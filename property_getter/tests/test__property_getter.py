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

    def test_single_key_in_list(self, component):
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

    def test_top_level_wildcard(self, component):
        input_data = {
            "name": "Alice",
            "age": 25,
            "city": "Los Angeles"
        }
        selected_property = "*"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == ["Alice", 25, "Los Angeles"]

    def test_wildcard_in_dictionary(self, component):
        input_data = {
            "user1": {"name": "Alice"},
            "user2": {"name": "Bob"},
            "user3": {"name": "Charlie"}
        }
        selected_property = "*.name"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == ["Alice", "Bob", "Charlie"]

    def test_wildcard_at_any_level(self, component):
        input_data = {
            "company": {
                "departments": {
                    "engineering": {
                        "employees": [
                            {"name": "Alice", "role": "Engineer"},
                            {"name": "Bob", "role": "Engineer"}
                        ]
                    },
                    "hr": {
                        "employees": [
                            {"name": "Charlie", "role": "HR"},
                            {"name": "Diana", "role": "HR"}
                        ]
                    }
                }
            }
        }
        selected_property = "company.departments.*.employees.*.name"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == ["Alice", "Bob", "Charlie", "Diana"]

    def test_empty_input_dict(self, component):
        input_data = {}
        selected_property = "name"
        with pytest.raises(ValueError):
            component.run(input=input_data, selected_property=selected_property)

    def test_empty_input_list(self, component):
        input_data = []
        selected_property = "0"
        with pytest.raises(ValueError):
            component.run(input=input_data, selected_property=selected_property)

    def test_empty_selected_property(self, component):
        input_data = {
            "name": "Alice",
            "age": 25,
            "city": "Los Angeles"
        }
        selected_property = ""
        with pytest.raises(ValueError):
            component.run(input=input_data, selected_property=selected_property)

    def test_non_string_keys_in_dict(self, component):
        input_data = {
            1: "Alice",
            2: "Bob",
            3: "Charlie"
        }
        selected_property = "2"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == "Bob"

    def test_deeply_nested_structures(self, component):
        input_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "name": "Deep"
                        }
                    }
                }
            }
        }
        selected_property = "level1.level2.level3.level4.name"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == "Deep"

    def test_wildcard_with_empty_list(self, component):
        input_data = {
            "users": []
        }
        selected_property = "users.*.name"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == []

    def test_wildcard_with_empty_dict(self, component):
        input_data = {
            "users": {}
        }
        selected_property = "users.*.name"
        output = component.run(input=input_data, selected_property=selected_property)
        assert output == []