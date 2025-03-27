from nl2sql.services.ai import AIService
from nl2sql.retrievers.context_retriever import ContextRetriever
from nl2sql.prompts import GenerateSQLQueryPrompt, DoubleCheckQueryPrompt



class Generator:
    def __init__(self, ai_service: AIService, context_retriever: ContextRetriever) -> None:
        self.ai_service = ai_service
        self.context_retriever = context_retriever

        self.generator_prompt = GenerateSQLQueryPrompt(self.ai_service)
        self.double_check_prompt = DoubleCheckQueryPrompt(self.ai_service)



    def generate(self, nl_query: str) -> str:
        context = self.context_retriever.retrieve(nl_query)

        table_attributes_context = ""
        sample_data_context = ""

        for table in context["relevant_tables"]:
            sample_table_data = context["relevant_sample_data"][table]

            table_attributes_context += f"- Table: {table}"

            attributes = []
            for value in context["relevant_attributes"]:
                if value["table"] == table:
                    for attribute in value["attributes"]:
                        attributes.append(f"`{attribute}`")

                        attribute_sample_data = sample_table_data[attribute].to_list()
                        sample_data_context += f"`{table}.{attribute}` = {', '.join([f'{value}' for value in attribute_sample_data])}\n"

            if len(attributes) > 0:
                table_attributes_context += f"; Attributes: {', '.join(attributes)}"

            table_attributes_context += "\n"

        reference_values_context = ""

        for entry in context["reference_values"]:
            reference_values_context += f"`{entry['table']}.{entry['attribute']}` = {', '.join([f'{value}' for value in entry['values']])}\n"

        sql_query = self.generator_prompt.run(
            nl_query, table_attributes_context, reference_values_context, sample_data_context
        )

        return self.double_check_prompt.run(
            nl_query, sql_query, context["relevant_nl_db_schema"]
        )
            


            
            
                        
        
        
