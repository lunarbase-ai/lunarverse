from lunar_nl2sql.services.ai import AIService

from pydantic import BaseModel

class ResponseFormat(BaseModel):
    sql: str

class DoubleCheckQueryPrompt:
    USER_MESSAGE= """
    Given the following natural language query, the generated SQL query, and a natural language 
    description of the database schema, double check if the SQL query is correct and return 
    the SQL query, corrected if needed.
    
    Natural Language Query: {nl_query}
    SQL Query: {sql_query}
    NL DB Schema Description: {nl_db_schema_description}


    Expected Output in json format:
    {{
    
        "sql": "<sql_query>"
    }}

    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def run(self, nl_query: str, sql_query: str, nl_db_schema_description: str):
        prompt = self.USER_MESSAGE.format(nl_query=nl_query, sql_query=sql_query, nl_db_schema_description=nl_db_schema_description)

        response = self.ai_service.run(messages=[{"role": "user", "content": prompt}], type="json", response_format=ResponseFormat)
        value = response.choices[0].message.parsed
        return value.sql