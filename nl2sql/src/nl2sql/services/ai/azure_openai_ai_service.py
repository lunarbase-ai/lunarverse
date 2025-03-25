from .base import AIService
from openai import AzureOpenAI


class AzureOpenAIService(AIService):
    def __init__(self, configuration: dict):    
        super().__init__()
        self.configuration = configuration

    def connect(self) -> None:
        if self._client is None:
            self._client = AzureOpenAI(
                api_key=self.configuration["openai_api_key"],
                api_version=self.configuration["openai_api_version"],
                endpoint=self.configuration["azure_endpoint"],
            )

    def run(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                messages=messages, 
                model=self.configuration["model"],
                **kwargs
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise e