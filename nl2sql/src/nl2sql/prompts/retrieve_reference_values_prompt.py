from nl2sql.services.ai import AIService
from pydantic import BaseModel

class ReferenceValue(BaseModel):
    table: str
    attribute: str
    values: list[str]

class ResponseFormat(BaseModel):
    references: list[ReferenceValue]

    class Config:
        json_schema_extra = {
            "type": "object",
            "properties": {
                "references": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "table": {"type": "string"},
                            "attribute": {"type": "string"},
                            "values": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["table", "values"]
                    }
                }
            },
            "required": ["references"]
        }


class RetrieveReferenceValuesPrompt:
    USER_MESSAGE = """
    Given the following natural language query to be mapped to an SQL query:
    {nl_query}
    
    Determine the set of references to values in the table, i.e. terms which are likely to map to VALUES in a WHERE = ‘VALUE’ clause.

    For reference, you have the following natural language description of the tables and their attributes:
    {description} 

    And the set of relevant tables and attributes for the SQL query:
    {relevant_tables_and_attributes}

    Expected Output:
    {{
    
        "references": [
            {{"table": "table_1", "attribute": "attribute_1", "values": ["value_1", "value_2"]}},
            {{"table": "table_1", "attribute": "attribute_2", "values": ["value_3", "value_4"]}},
            {{"table": "table_2", "attribute": "attribute_3", "values": ["value_5"]}}
        ]
    }}
    """
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def run(self, nl_query: str, description: dict[str, str], relevant_tables_and_attributes: dict[str, list[str]]):
        prompt = self.USER_MESSAGE.format(nl_query=nl_query, description=description, relevant_tables_and_attributes=relevant_tables_and_attributes)
        response = self.ai_service.run(messages=[
            {"role": "user", "content": prompt},
        ], type="json", response_format=ResponseFormat)
        value = response.choices[0].message.parsed
        return [item.model_dump() for item in value.references]



