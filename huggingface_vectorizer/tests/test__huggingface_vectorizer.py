import pytest
from unittest.mock import patch, MagicMock
from huggingface_vectorizer import HuggingfaceVectorizer
from lunarcore.component.data_types import EmbeddedText

class TestHuggingfaceVectorizer:
    def setup_method(self):
        self.vectorizer = HuggingfaceVectorizer()
        self.valid_model_name = "bert-base-uncased"
        self.invalid_model_name = "invalid-model"

    @patch('huggingface_vectorizer.HuggingFaceEmbeddings')
    def test_run_returns_correct_embeddings_for_single_text(self, MockHuggingFaceEmbeddings):
        mock_embeddings_instance = MockHuggingFaceEmbeddings.return_value
        mock_embeddings_instance.embed_documents.return_value = [[0.1, 0.2, 0.3]]
        
        text = "Hello world"
        result = self.vectorizer.run(text, self.valid_model_name)
        
        assert len(result) == 1
        assert isinstance(result[0], EmbeddedText)
        assert result[0].text == text
        assert result[0].embeddings == [0.1, 0.2, 0.3]

    @patch('huggingface_vectorizer.HuggingFaceEmbeddings')
    def test_run_returns_correct_embeddings_for_multiple_texts(self, MockHuggingFaceEmbeddings):
        mock_embeddings_instance = MockHuggingFaceEmbeddings.return_value
        mock_embeddings_instance.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        
        texts = ["Hello world", "Goodbye world"]
        result = self.vectorizer.run(texts, self.valid_model_name)
        
        assert len(result) == 2
        assert isinstance(result[0], EmbeddedText)
        assert result[0].text == texts[0]
        assert result[0].embeddings == [0.1, 0.2, 0.3]
        assert isinstance(result[1], EmbeddedText)
        assert result[1].text == texts[1]
        assert result[1].embeddings == [0.4, 0.5, 0.6]

    @patch('huggingface_vectorizer.HuggingFaceEmbeddings')
    def test_run_handles_empty_text_list(self, MockHuggingFaceEmbeddings):
        mock_embeddings_instance = MockHuggingFaceEmbeddings.return_value
        mock_embeddings_instance.embed_documents.return_value = []
        
        texts = []
        result = self.vectorizer.run(texts, self.valid_model_name)
        
        assert result == []

    @patch('huggingface_vectorizer.HuggingFaceEmbeddings')
    def test_run_handles_empty_string(self, MockHuggingFaceEmbeddings):
        mock_embeddings_instance = MockHuggingFaceEmbeddings.return_value
        mock_embeddings_instance.embed_documents.return_value = [[]]
        
        text = ""
        result = self.vectorizer.run(text, self.valid_model_name)
        
        assert len(result) == 1
        assert isinstance(result[0], EmbeddedText)
        assert result[0].text == text
        assert result[0].embeddings == []

    @patch('huggingface_vectorizer.HuggingFaceEmbeddings')
    def test_run_raises_error_for_invalid_model_name(self, MockHuggingFaceEmbeddings):
        mock_embeddings_instance = MockHuggingFaceEmbeddings.return_value
        mock_embeddings_instance.embed_documents.side_effect = ValueError("Invalid model name")
        
        text = "Hello world"
        with pytest.raises(ValueError, match="Model invalid-model not found. Please check the model name."):
            self.vectorizer.run(text, self.invalid_model_name)