from lunar_nl2sql.services.ai import AIService

from pydantic import BaseModel


class ResponseFormat(BaseModel):
    sql: str


class GenerateSQLQueryPrompt:
    USER_MESSAGE = """
    Given the natural language query: {nl_query}
    
    the set of relevant tables, attributes:
    {table_attributes_context}

    the set of target/reference values:
    {reference_values_context}

    the set of sample data:
    {sample_data_context}

    Write the corresponding SQL query.
    Build the SQL query in a step-wise manner:
    Determine the table and the projection attributes.
    Determine the select statement clauses.
    Determine the joins.
    Define the aggregation operations (if applicable).

    Return only the SQL query in a json object.

    Example Output:
    {{
        "sql": "<SQL Query>"
    }}
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def run(
        self,
        nl_query: str,
        table_attributes_context: str,
        reference_values_context: str,
        sample_data_context: str,
    ):
        prompt = self.USER_MESSAGE.format(
            nl_query=nl_query,
            table_attributes_context=table_attributes_context,
            reference_values_context=reference_values_context,
            sample_data_context=sample_data_context,
        )

        response = self.ai_service.run(
            messages=[{"role": "user", "content": prompt}],
            type="json",
            response_format=ResponseFormat,
        )
        value = response.choices[0].message.parsed
        return value.sql
