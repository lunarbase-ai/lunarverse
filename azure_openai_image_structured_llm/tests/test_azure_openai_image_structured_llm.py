import pytest
from unittest.mock import Mock, patch
from azure_openai_image_structured_llm import AzureOpenAIImageStructuredLLM
from lunarcore.component.data_types import File, Base64FileContent
import json


MOCK_CONFIG = {
    "openai_api_key": "fake-key",
    "openai_api_version": "2024-02-15-preview",
    "azure_endpoint": "https://fake-endpoint.openai.azure.com/",
    "deployment_name": "fake-deployment"
}

MOCK_IMAGE = File(
    content=Base64FileContent(
        type="base64",
        content="fake-base64-content"
    )
)

VALID_SCHEMA = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "confidence": {"type": "number"}
    },
    "required": ["description", "confidence"]
}

MOCK_LLM_RESPONSE = {
    "description": "A test image",
    "confidence": 0.95
}

@pytest.fixture
def component():
    with patch('azure_openai_image_structured_llm.AzureOpenAI') as mock_client:
        mock_response = Mock()
        mock_response.choices = [
            Mock(
                message=Mock(
                    content=json.dumps(MOCK_LLM_RESPONSE)
                )
            )
        ]
        mock_client.return_value.chat.completions.create.return_value = mock_response

        component = AzureOpenAIImageStructuredLLM(**MOCK_CONFIG)
        return component

def test_init():
    with patch('azure_openai_image_structured_llm.AzureOpenAI') as mock_client:
        component = AzureOpenAIImageStructuredLLM(**MOCK_CONFIG)
        assert component.configuration == MOCK_CONFIG
        mock_client.assert_called_once_with(
            api_key=MOCK_CONFIG["openai_api_key"],
            api_version=MOCK_CONFIG["openai_api_version"],
            azure_endpoint=MOCK_CONFIG["azure_endpoint"]
        )

def test_run_success(component):
    result = component.run(
        user_prompt="Describe this image",
        image=MOCK_IMAGE,
        schema=VALID_SCHEMA
    )
    
    assert result == MOCK_LLM_RESPONSE
    
    component._client.chat.completions.create.assert_called_once()
    call_args = component._client.chat.completions.create.call_args[1]
    assert call_args["model"] == MOCK_CONFIG["deployment_name"]
    assert call_args["response_format"] == {"type": "json_schema", "json_schema": VALID_SCHEMA}
    
    messages = call_args["messages"]
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert len(messages[1]["content"]) == 2
    assert messages[1]["content"][0]["type"] == "text"
    assert messages[1]["content"][1]["type"] == "image_url"
    assert "data:image;base64,fake-base64-content" in messages[1]["content"][1]["image_url"]["url"]

def test_invalid_image_type(component):
    invalid_image = {
        "content": {
            "type": "invalid",
            "content": "fake-content"
        }
    }
    
    with pytest.raises(ValueError, match="Image content type must be base64"):
        component.run(
            user_prompt="Describe this image",
            image=invalid_image,
            schema=VALID_SCHEMA
        )

def test_invalid_schema(component):
    invalid_schema = {"type": "invalid"}
    
    with pytest.raises(ValueError, match="JSON schema is invalid"):
        component.run(
            user_prompt="Describe this image",
            image=MOCK_IMAGE,
            schema=invalid_schema
        )

def test_invalid_json_response(component):
    mock_response = Mock()
    mock_response.choices = [
        Mock(
            message=Mock(
                content="invalid json"
            )
        )
    ]
    component._client.chat.completions.create.return_value = mock_response
    
    with pytest.raises(ValueError, match="Error decoding JSON"):
        component.run(
            user_prompt="Describe this image",
            image=MOCK_IMAGE,
            schema=VALID_SCHEMA
        )

def test_empty_response(component):
    mock_response = Mock()
    mock_response.choices = []
    component._client.chat.completions.create.return_value = mock_response
    
    with pytest.raises(ValueError, match="Error executing Azure OpenAI Image Structured LLM"):
        component.run(
            user_prompt="Describe this image",
            image=MOCK_IMAGE,
            schema=VALID_SCHEMA
        )

def test_custom_system_prompt(component):
    custom_prompt = "You are a specialized image analyzer"
    component.run(
        user_prompt="Describe this image",
        image=MOCK_IMAGE,
        schema=VALID_SCHEMA,
        system_prompt=custom_prompt
    )
    
    call_args = component._client.chat.completions.create.call_args[1]
    messages = call_args["messages"]
    assert messages[0]["content"] == custom_prompt