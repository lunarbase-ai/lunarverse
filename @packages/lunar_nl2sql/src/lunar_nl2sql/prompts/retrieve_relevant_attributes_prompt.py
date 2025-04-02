from lunar_nl2sql.services.ai import AIService
from pydantic import BaseModel
from typing import List, Dict, Any


class TableAttributePair(BaseModel):
    table: str
    attributes: List[str]


class ResponseFormat(BaseModel):
    table_attributes: List[TableAttributePair]

    class Config:
        json_schema_extra = {
            "type": "object",
            "properties": {
                "table_attributes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "table": {"type": "string"},
                            "attributes": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["table", "attributes"],
                    },
                }
            },
            "required": ["table_attributes"],
        }


class RetrieveRelevantTableAttributesPrompt:
    USER_MESSAGE = """
    Select from a JSON array where each element contains a "table" key with the table name and an "attributes" key with a list of relevant attributes to answer the following natural language query: {nl_query}

    Natural Language Description of the tables and its attributes:
    {description} 

    ## Example Output:
    {{
        "table_attributes": [
            {{"table": "table_1", "attributes": ["attribute_1", "attribute_2"]}},
            {{"table": "table_2", "attributes": ["attribute_3"]}}
        ]
    }}
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def run(self, nl_query: str, description: str) -> List[Dict[str, Any]]:
        prompt = self.USER_MESSAGE.format(nl_query=nl_query, description=description)

        response = self.ai_service.run(
            messages=[{"role": "user", "content": prompt}],
            type="json",
            response_format=ResponseFormat,
        )

        value = response.choices[0].message.parsed
        return [item.model_dump() for item in value.table_attributes]
