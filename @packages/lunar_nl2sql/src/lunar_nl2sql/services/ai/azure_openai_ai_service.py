from .base import AIService
from openai import AzureOpenAI
from typing import List, Dict, Any


class AzureOpenAIService(AIService):
    def __init__(self, configuration: dict):    
        super().__init__()
        self.configuration = configuration

    def connect(self) -> None:
        if self._client is None:
            self._client = AzureOpenAI(
                api_key=self.configuration["openai_api_key"],
                api_version=self.configuration["openai_api_version"],
                azure_endpoint=self.configuration["azure_endpoint"],
            )

    def run(self, messages: List[Dict[str, str]], type: str = "text", **kwargs):
        if type == "text":
            return self.run_text(messages, **kwargs)

        elif type == "json":
            return self.run_json(messages, **kwargs)

        else:
            return self.run_text(messages, **kwargs)

    def run_json(self, messages: List[Dict[str, str]], **kwargs):
        try:
            return self.client.beta.chat.completions.parse(
                messages=messages, 
                model=self.configuration["model"],
                **kwargs
            )
        except Exception as e:
            raise e
    
    def run_text(self, messages: List[Dict[str, str]], **kwargs):
        try:
            return self.client.chat.completions.create(
                messages=messages, 
                model=self.configuration["model"],
                **kwargs
            )
        except Exception as e:
            raise e