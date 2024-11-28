from unittest.mock import patch
from azure_openai_vectorizer import AzureOpenAIVectorizer
from lunarcore.component.data_types import EmbeddedText

class TestAzureOpenAIVectorizer:

    def setup_method(self):
        self.env_patcher = patch.dict('os.environ', {
            'OPENAI_API_VERSION': 'v1',
            'AZURE_OPENAI_VECTORIZER_DEPLOYMENT_NAME': 'deployment_name',
            'OPENAI_API_KEY': 'api_key',
            'AZURE_OPENAI_ENDPOINT': 'endpoint',
            'AZURE_OPENAI_VECTORIZER_MODEL': 'model_name'
        })
        self.env_patcher.start()

        self.mock_azure_openai_embeddings = patch('azure_openai_vectorizer.AzureOpenAIEmbeddings')
        self.MockAzureOpenAIEmbeddings = self.mock_azure_openai_embeddings.start()
        self.mock_client = self.MockAzureOpenAIEmbeddings.return_value

    def teardown_method(self):
        self.env_patcher.stop()
        self.mock_azure_openai_embeddings.stop()

    def test_run(self):
        self.mock_client.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        
        vectorizer = AzureOpenAIVectorizer()
        documents = ["text1", "text2"]
        
        result = vectorizer.run(documents)
        
        expected_result = [
            EmbeddedText(embeddings=[0.1, 0.2, 0.3], text="text1").dict(),
            EmbeddedText(embeddings=[0.4, 0.5, 0.6], text="text2").dict()
        ]
        assert result == expected_result
        self.mock_client.embed_documents.assert_called_once_with(documents)

    def test_run_empty_documents(self):
        self.mock_client.embed_documents.return_value = []
        
        vectorizer = AzureOpenAIVectorizer()
        documents = []
        
        result = vectorizer.run(documents)
        
        expected_result = []
        assert result == expected_result
        self.mock_client.embed_documents.assert_called_once_with(documents)

    def test_run_single_document(self):
        self.mock_client.embed_documents.return_value = [[0.1, 0.2, 0.3]]
        
        vectorizer = AzureOpenAIVectorizer()
        documents = ["text1"]
        
        result = vectorizer.run(documents)
        
        expected_result = [
            EmbeddedText(embeddings=[0.1, 0.2, 0.3], text="text1").dict()
        ]
        assert result == expected_result
        self.mock_client.embed_documents.assert_called_once_with(documents)

    def test_run_with_special_characters(self):
        self.mock_client.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        
        vectorizer = AzureOpenAIVectorizer()
        documents = ["text1!@#", "text2$%^"]
        
        result = vectorizer.run(documents)
        
        expected_result = [
            EmbeddedText(embeddings=[0.1, 0.2, 0.3], text="text1!@#").dict(),
            EmbeddedText(embeddings=[0.4, 0.5, 0.6], text="text2$%^").dict()
        ]
        assert result == expected_result
        self.mock_client.embed_documents.assert_called_once_with(documents)