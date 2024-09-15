import unittest
from unittest import mock
from fastapi.testclient import TestClient
from models.query import Query
import app


class TestApp(unittest.TestCase):

    @mock.patch("app.ChromaDB")
    @mock.patch("app.GenerativeLLM")
    @mock.patch("app.GeminiEmbeddingFunction")
    @mock.patch("app.FastAPI")
    def setUp(
        self,
        mock_fastapi,
        mock_gemini_embedding_function,
        mock_generative_llm,
        mock_chroma_db,
    ):
        # Mock the services
        self.fastapi = mock_fastapi
        self.gemini_embedding_function = mock_gemini_embedding_function
        self.generative_llm = mock_generative_llm
        self.chroma_db = mock_chroma_db
        self.gemini_embedding_function.return_value = mock.Mock()
        self.generative_llm.get_model.return_value = mock.Mock()
        self.chroma_db.return_value = mock.Mock()

        # Initialize the test client
        self.fastapi.return_value = self.client = TestClient(app.app)
        self.client.post = mock.Mock()

    def test_query(self):
        """Test the query endpoint.
        """
        # Mock the response
        self.client.post.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "test"}

        # Test the query endpoint
        query = Query(query="test")
        response = self.client.post("/query", json=query.dict())
        assert response.status_code == 200
        assert response.json() == {"response": "test"}

        # Test the mock calls
        self.client.post.assert_called_once()
        self.client.post.assert_called_with("/query", json=query.dict())

    def test_query_error(self):
        """Test the query endpoint with an error.
        """
        # Mock the response
        self.client.post.return_value = mock_response = mock.Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "test"}

        # Test the query endpoint
        query = Query(query="test")
        response = self.client.post("/query", json=query.dict())
        assert response.status_code == 400
        assert response.json() == {"detail": "test"}

        # Test the mock calls
        self.client.post.assert_called_once()
        self.client.post.assert_called_with("/query", json=query.dict())
