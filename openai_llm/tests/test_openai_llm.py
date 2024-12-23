from unittest.mock import patch, MagicMock
from openai_llm import OpenAiPrompt

class TestOpenAiPrompt:

    def setup_method(self):
        self.env_atcher = patch.dict('os.environ', {
            'OPENAI_API_KEY': 'openai_api_key',
            'OPENAI_MODEL': 'openai_model'
        })

        self.env_patcher.start()

        self.mock_openai_chat_ai = patch('openai.OpenAI')
        self.MockOpenAI = self.mock_openai_chat_ai.start
        self.mock_client = self.MockOpenAI.return_value


    def teardown_method(self):
        self.env_patcher.stop()
        self.mock_openai_chat_ai.stop()

    def test_run_with_default_system_prompt(self):
        mock_response = MagicMock()
        mock_response.content = "response"
        self.mock_client.chat.completions.create.return_value = mock_response

        prompt = OpenAiPrompt()
        user_prompt = "Hello"
        system_prompt = "System prompt"

        result = prompt.run(user_prompt, system_prompt)

        expected_result = "response"
        assert result == expected_result
        self.mock_client.chat.completions.create.assert_called_once_with(messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])