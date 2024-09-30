# ReACT Agent

## Overview
The **ReACT Agent** is a software component designed to implement ReACT logic, providing the ability to process a given query using a set of tools. This component leverages OpenAI's API and can be configured to enable or disable the use of unsupported tools.

## Input Types
The **ReACT Agent** accepts the following input types:
- `Query`: A `TEXT` input representing the query or question that needs to be processed.
- `Tools`: A `LIST` input containing the tools available for processing the query.

## Output Type
The output of the **ReACT Agent** is a single `TEXT` response that answers the input query, utilizing the provided tools.

## Configuration Parameters
The **ReACT Agent** can be configured using the following parameters:
- `tools_config`: Configuration settings for the tools that the agent can use.
- `openai_api_key`: The API key required to access OpenAI's services.
- `enable_unsupported_tools`: A boolean flag that enables or disables the use of tools that are not officially supported.

## Usage
To use the **ReACT Agent**, you need to provide it with the necessary inputs (Query and Tools) and configure it with the appropriate parameters (tools_config, openai_api_key, and enable_unsupported_tools). The agent will then process the query using the available tools and return a textual response based on the input query.

## Contributing
If you would like to contribute to the development of the **ReACT Agent**, please follow the standard guidelines for contributing to the project, ensuring that all code adheres to the project's coding standards and is thoroughly tested.

## License
The **ReACT Agent** is distributed under the terms of the applicable license, which can be found in the LICENSE file in the root directory of the project.

For further information or support, please refer to the project's documentation or contact the maintainer.