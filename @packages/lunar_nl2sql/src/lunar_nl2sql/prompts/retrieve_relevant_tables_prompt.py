from lunar_nl2sql.services.ai import AIService
from pydantic import BaseModel


class ResponseFormat(BaseModel):
    tables: list[str]


class RetrieveRelevantTablesPrompt:
    USER_MESSAGE = """
    Select from a json where the keys are the tables, and the values are the natural language schema description of the table and its attributes, the tables which are relevant to answer the following natural language query: {nl_query}

    Instructions:
    Just return the list of table names in a json object.

    Natural Language Description of the tables and its attributes:
    {description}

    ## Example Output:
  {{
        "tables": ["table1", "table2"]
    }}
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def run(self, nl_query: str, description: str) -> list[str]:
        prompt = self.USER_MESSAGE.format(nl_query=nl_query, description=description)

        response = self.ai_service.run(
            messages=[
                {"role": "user", "content": prompt},
            ],
            type="json",
            response_format=ResponseFormat,
        )
        value = response.choices[0].message.parsed
        return value.tables
