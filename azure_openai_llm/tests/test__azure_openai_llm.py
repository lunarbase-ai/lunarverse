from unittest.mock import patch, MagicMock
from azure_openai_llm import AzureOpenAIPrompt
from langchain.schema import SystemMessage, HumanMessage

class TestAzureOpenAIPrompt:

    def setup_method(self):
        # Patch environment variables
        self.env_patcher = patch.dict('os.environ', {
            'OPENAI_API_VERSION': 'v1',
            'DEPLOYMENT_NAME': 'test-deployment',
            'OPENAI_API_KEY': 'mock-api-key',
            'AZURE_OPENAI_ENDPOINT': 'https://mockendpoint.azure.com'
        })
        self.env_patcher.start()

        self.mock_azure_openai_chat_ai = patch('azure_openai_llm.AzureChatOpenAI')
        self.MockAzureChatOpenAI = self.mock_azure_openai_chat_ai.start()
        self.mock_client = self.MockAzureChatOpenAI.return_value

    def teardown_method(self):
        self.env_patcher.stop()
        self.mock_azure_openai_chat_ai.stop()

    def test_run_with_default_system_prompt(self):
        mock_response = MagicMock()
        mock_response.content = "response"
        self.mock_client.invoke.return_value = mock_response
        
        prompt = AzureOpenAIPrompt()
        user_prompt = "Hello"
        system_prompt = "System prompt"
        
        result = prompt.run(user_prompt, system_prompt)
        
        expected_result = "response"
        assert result == expected_result
        self.mock_client.invoke.assert_called_once_with(input=[
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

    def test_run_with_custom_system_prompt(self):
        mock_response = MagicMock()
        mock_response.content = "custom response"
        self.mock_client.invoke.return_value = mock_response
        
        prompt = AzureOpenAIPrompt()
        user_prompt = "Hi"
        system_prompt = "Custom system prompt"
        
        result = prompt.run(user_prompt, system_prompt)
        
        expected_result = "custom response"
        assert result == expected_result
        self.mock_client.invoke.assert_called_once_with(input=[
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

    def test_run_with_empty_response(self):
        mock_response = MagicMock()
        mock_response.content = ""
        self.mock_client.invoke.return_value = mock_response
        
        prompt = AzureOpenAIPrompt()
        user_prompt = "Hello"
        system_prompt = "System prompt"
        
        result = prompt.run(user_prompt, system_prompt)
        
        expected_result = ""
        assert result == expected_result
        self.mock_client.invoke.assert_called_once_with(input=[
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

    def test_run_with_special_characters(self):
        mock_response = MagicMock()
        mock_response.content = "response with special characters"
        self.mock_client.invoke.return_value = mock_response
        
        prompt = AzureOpenAIPrompt()
        user_prompt = "Hello!@#"
        system_prompt = "System prompt$%^"
        
        result = prompt.run(user_prompt, system_prompt)
        
        expected_result = "response with special characters"
        assert result == expected_result
        self.mock_client.invoke.assert_called_once_with(input=[
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])