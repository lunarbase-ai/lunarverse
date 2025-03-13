from unittest.mock import patch
import os
from azure_openai_llm.src.azure_openai_llm import AzureOpenAIPrompt

class TestAzureOpenAIPrompt:

    def setup_method(self):
        # Patch environment variables
        self.env_patcher = patch.dict(os.environ, {
            'OPENAI_API_VERSION': 'v1',
            'DEPLOYMENT_NAME': 'test-deployment',
            'OPENAI_API_KEY': 'mock-api-key',
            'AZURE_OPENAI_ENDPOINT': 'https://mockendpoint.azure.com'
        })
        self.env_patcher.start()

        # Patch openai.ChatCompletion.create
        self.chat_completion_patcher = patch('openai.ChatCompletion.create')
        self.mock_chat_completion_create = self.chat_completion_patcher.start()

    def teardown_method(self):
        self.env_patcher.stop()
        self.chat_completion_patcher.stop()

    def test_run_with_default_system_prompt(self):
        # Prepare the mock response in the expected format.
        mock_response = {"choices": [{"message": {"content": "response"}}]}
        self.mock_chat_completion_create.return_value = mock_response

        prompt = AzureOpenAIPrompt()
        prompt.configuration = {
            'openai_api_version' : 'v1',
            'deployment_name' : 'test-deployment',
            'openai_api_key' : 'mock-api-key',
            'azure_endpoint' : 'https://mockendpoint.azure.com',
        }
        user_prompt = "Hello"
        system_prompt = "System prompt"

        result = prompt.run(user_prompt, system_prompt)

        expected_result = "response"
        assert result == expected_result

        expected_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        self.mock_chat_completion_create.assert_called_once_with(
            engine='test-deployment',
            messages=expected_messages,
        )

    def test_run_with_custom_system_prompt(self):
        mock_response = {"choices": [{"message": {"content": "custom response"}}]}
        self.mock_chat_completion_create.return_value = mock_response

        prompt = AzureOpenAIPrompt()
        prompt.configuration = {
            'openai_api_version' : 'v1',
            'deployment_name' : 'test-deployment',
            'openai_api_key' : 'mock-api-key',
            'azure_endpoint' : 'https://mockendpoint.azure.com',
        }
        user_prompt = "Hi"
        system_prompt = "Custom system prompt"

        result = prompt.run(user_prompt, system_prompt)

        expected_result = "custom response"
        assert result == expected_result

        expected_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        self.mock_chat_completion_create.assert_called_once_with(
            engine='test-deployment',
            messages=expected_messages,
        )

    def test_run_with_empty_response(self):
        mock_response = {"choices": [{"message": {"content": ""}}]}
        self.mock_chat_completion_create.return_value = mock_response

        prompt = AzureOpenAIPrompt()
        prompt.configuration = {
            'openai_api_version' : 'v1',
            'deployment_name' : 'test-deployment',
            'openai_api_key' : 'mock-api-key',
            'azure_endpoint' : 'https://mockendpoint.azure.com',
        }
        user_prompt = "Hello"
        system_prompt = "System prompt"

        result = prompt.run(user_prompt, system_prompt)

        expected_result = ""
        assert result == expected_result

        expected_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        self.mock_chat_completion_create.assert_called_once_with(
            engine='test-deployment',
            messages=expected_messages,
        )

    def test_run_with_special_characters(self):
        mock_response = {"choices": [{"message": {"content": "response with special characters"}}]}
        self.mock_chat_completion_create.return_value = mock_response

        prompt = AzureOpenAIPrompt()
        prompt.configuration = {
            'openai_api_version' : 'v1',
            'deployment_name' : 'test-deployment',
            'openai_api_key' : 'mock-api-key',
            'azure_endpoint' : 'https://mockendpoint.azure.com',
        }
        user_prompt = "Hello!@#"
        system_prompt = "System prompt$%^"

        result = prompt.run(user_prompt, system_prompt)

        expected_result = "response with special characters"
        assert result == expected_result

        expected_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        self.mock_chat_completion_create.assert_called_once_with(
            engine='test-deployment',
            messages=expected_messages,
        )
