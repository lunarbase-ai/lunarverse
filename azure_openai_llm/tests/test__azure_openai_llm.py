from unittest.mock import patch, MagicMock
from azure_openai_llm.src.azure_openai_llm import AzureOpenAIPrompt

class TestAzureOpenAIPrompt:

    def setup_method(self):
        self.config = {
            'openai_api_version': 'v1',
            'deployment_name': 'test-deployment',
            'openai_api_key': 'mock-api-key',
            'azure_endpoint': 'https://mockendpoint.azure.com',
        }

        self.mock_azure_openai = patch('azure_openai_llm.src.azure_openai_llm.AzureOpenAI')
        self.MockAzureOpenAI = self.mock_azure_openai.start()
        self.mock_client = self.MockAzureOpenAI.return_value

    def teardown_method(self):
        self.mock_azure_openai.stop()

    def test_run_with_default_system_prompt(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "response"
        self.mock_client.chat.completions.create.return_value = mock_response
        user_prompt = "Hello"
        system_prompt = "System prompt"
        expected_result = "response"

        prompt = AzureOpenAIPrompt()
        result = prompt.run(user_prompt, system_prompt)

        assert result == expected_result
        self.mock_client.chat.completions.create.assert_called_once_with(
            model='$LUNARENV::DEPLOYMENT_NAME',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

    def test_run_with_custom_system_prompt(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "custom response"
        self.mock_client.chat.completions.create.return_value = mock_response

        prompt = AzureOpenAIPrompt()
        user_prompt = "Hi"
        system_prompt = "Custom system prompt"

        result = prompt.run(user_prompt, system_prompt)

        expected_result = "custom response"
        assert result == expected_result
        self.mock_client.chat.completions.create.assert_called_once_with(
            model='$LUNARENV::DEPLOYMENT_NAME',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

    def test_run_with_empty_response(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = ""
        self.mock_client.chat.completions.create.return_value = mock_response

        prompt = AzureOpenAIPrompt()
        user_prompt = "Hello"
        system_prompt = "System prompt"

        result = prompt.run(user_prompt, system_prompt)

        expected_result = ""
        assert result == expected_result
        self.mock_client.chat.completions.create.assert_called_once_with(
            model='$LUNARENV::DEPLOYMENT_NAME',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

    def test_run_with_special_characters(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "response with special characters"
        self.mock_client.chat.completions.create.return_value = mock_response

        prompt = AzureOpenAIPrompt()
        user_prompt = "Hello!@#"
        system_prompt = "System prompt$%^"

        result = prompt.run(user_prompt, system_prompt)

        expected_result = "response with special characters"
        assert result == expected_result
        self.mock_client.chat.completions.create.assert_called_once_with(
            model='$LUNARENV::DEPLOYMENT_NAME',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
