### JSON Input

A JSON Input component enables sending JSON inputs to downstream components. The component consists of a text field that accepts JSON strings, potentially with template variables (e.g., `{"key": "{template_variable}"}`). The provided values will represent the output of the component. If the input is a template, the template variables will be replaced by their values at the output.

#### Inputs
As mentioned above, the input consists of a text field that accepts JSON strings with template variables.

| input name | input data type | example value | description |
|------------|-----------------|---------------|-------------|
| input      | text            | `{"name": "{name}"}` or `{"name": "Alex"}` | The value can be a simple JSON string or a templated JSON string where the template variable will be filled in as part of a different input |

#### Output
The component will output a JSON object - the input value, with the template variables replaced in the JSON string when they exist.

#### Example
See Lunar for an example of how to use this component in a workflow and much more.