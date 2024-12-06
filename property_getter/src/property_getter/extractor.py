from typing import Any, Dict, List, Union

class PropertyExtractor:
    def get_nested_value(self, value: Union[Dict, List], parts: List[str]) -> Any:
        if not parts:
            return value

        p = parts[0]
        if isinstance(value, list):
            return self._get_from_list(value, p, parts)
        elif isinstance(value, dict):
            return self._get_from_dict(value, p, parts)
        else:
            raise ValueError(f"Cannot navigate through non-dict and non-list value: {value}")

    def _get_from_list(self, value: List[Any], p: str, parts: List[str]) -> Any:
        if p.strip() == "*":
            result = [self.get_nested_value(item, parts[1:]) for item in value]
        else:
            try:
                index = int(p)
                result = self.get_nested_value(value[index], parts[1:])
            except (ValueError, IndexError):
                raise ValueError(f"Invalid index {p} for list!")
        
        if isinstance(result, list):
            return self.flatten(result)
        return result

    def _get_from_dict(self, value: Dict[Any, Any], p: str, parts: List[str]) -> Any:
        if p.strip() == "*":
            result = [self.get_nested_value(v, parts[1:]) for v in value.values()]
        else:
            try:
                result = self.get_nested_value(value[p], parts[1:])
            except KeyError:
                try:
                    key = int(p)
                    result = self.get_nested_value(value[key], parts[1:])
                except (ValueError, KeyError):
                    raise ValueError(f"The selected property <{p}> doesn't exist in the input object!")
        
        if isinstance(result, list):
            return self.flatten(result)
        return result


    def flatten(self, nested_list: List[Any]) -> List[Any]:
        flat_list = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list.extend(self.flatten(item))
            else:
                flat_list.append(item)
        return flat_list