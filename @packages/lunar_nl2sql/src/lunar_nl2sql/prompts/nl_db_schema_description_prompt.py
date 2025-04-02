from lunar_nl2sql.services.ai import AIService

class NLDBSchemaDescriptionPrompt:
    USER_MESSAGE="""
    Given the table sample below:
    Table name: {table_name}
    {sample}
    
    Create a list of with a description of the the table and attribute in the following format:
    Table name; natural language description of the table
    Attribute name; natural language description of the table; attribute type; format; primary key
    
    where:
    Attribute type contains the basic type of the attribute.
    Format contains a description of the value format (e.g. date format, separators, etc).
    Primary key: a boolean true | false in case the attribute is likely to be a primary key.
    
    Important: 
    Must do it for all attributes. Just return the list.
    Do not return the original table sample.
    
    """
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service


    def run(self, table_name: str, sample: str) -> str:
        response = self.ai_service.run(messages=[
            {"role": "user", "content": self.USER_MESSAGE.format(table_name=table_name, sample=sample)},
        ])

        return response.choices[0].message.content.strip()
