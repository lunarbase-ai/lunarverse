from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType, File
from openai import AzureOpenAI
from typing import Any
from jsonschema import Draft7Validator, SchemaError
import json

SYSTEM_PROMPT = "You are a helpful AI assistant. Your name is AI Rover."

class AzureOpenAIImageStructuredLLM(
    LunarComponent,
    component_name="Azure Open AI Image Structured LLM",
    component_description="""Connects to Azure OpenAI's API (an LLM), runs an inputted natural language prompt that analyzes an image (str), and output the result as text (str)""",
    input_types={"user_prompt": DataType.TEMPLATE, "system_prompt": DataType.TEMPLATE, "image": DataType.FILE, "schema": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.GENAI,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT",
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self._client = AzureOpenAI(
            api_key=self.configuration["openai_api_key"],
            api_version=self.configuration["openai_api_version"],
            azure_endpoint=self.configuration["azure_endpoint"]
        )

    def run(self, user_prompt: str,  image: File, schema: dict, system_prompt: str = SYSTEM_PROMPT):
        if image.content.type is not "base64":
            raise ValueError("Image content type must be base64")
        try:
            Draft7Validator.check_schema(schema)
        except SchemaError as e:
            raise ValueError(f"JSON schema is invalid: {e.message}")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image;base64,{image.content.content}"}}
            ]}
        ]
        response = self._client.chat.completions.create(
            model=self.configuration["deployment_name"],
            messages=messages,
            response_format={"type": "json_schema", "json_schema": schema}
        )
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            json_string = response.choices[0].message.content
            try:
                parsed_json = json.loads(json_string)
                return parsed_json
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON: {e}")
        else:
            raise ValueError("Error executing Azure OpenAI Image Structured LLM")