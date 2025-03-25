from nl2sql.services.ai import AIService

class NLTableSummaryPrompt:
    USER_MESSAGE="""
    Given the schema description below, provide a summary description of the table limited to 3 sentences.
    {schema_description}
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def run(self, schema_description: str) -> str:
        response = self.ai_service.run(messages=[
            {"role": "user", "content": self.USER_MESSAGE.format(schema_description=schema_description)},
        ])

        return response.choices[0].message.content.strip()