"""Module to define the GeminiEmbeddingFunction class."""
# Standard Library
import logging
from typing import Optional, Union, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Third-Party
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Third-Party
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from chromadb import EmbeddingFunction, Documents

# Local Folder
from utils import enums
from models.document import Document


class GeminiEmbeddingFunction(EmbeddingFunction):
    """Generates embeddings for text documents using Google's Text Embedding
    API and stores them in a ChromaDB collection.
    """
    def __init__(
        self,
        model_name: Optional[str] = enums.EMBEDDING_MODEL,
        output_dimensionality: Optional[int] = enums.OUTPUT_DIMENSIONALITY,
    ) -> None:
        """Initializes the EmbeddingGenerator with a GenerativeModel instance
        and a PersistentClient instance for storing embeddings.

        Parameters
        ----------
        model_name : Optional[str], optional
            The name of the text embedding model to use, by default
            "models/text-embedding-004"
        output_dimensionality : Optional[int], optional
            The size of the output embeddings, by default 768
        """
        super().__init__()
        self.model_name = model_name
        self.output_dimensionality = output_dimensionality
        self.embedding_function = GoogleGenerativeAIEmbeddings(
            model=model_name,
            task_type="retrieval_document",
        )

    def __call__(
        self, input: Union[Documents, List[Document], List[str], str]
    ) -> List[List[float]]:
        """Generates embeddings for the input text documents.

        Parameters
        ----------
        input : Union[Documents, List[Document], List[str], str]
            The input text documents to generate embeddings for.

        Returns
        -------
        List[List[float]]
            The embeddings for the input text documents.
        """
        # Convert input to a list of strings
        if isinstance(input, str):
            input = [input]
        elif (
            isinstance(input, list)
            and len(input) > 0
            and isinstance(input[0], Document)
        ):
            input = [doc.page_content for doc in input]

        return self.embedding_function.embed_documents(
            texts=input,
            output_dimensionality=self.output_dimensionality,
        )

    def embed_documents(
        self, documents: Union[Documents, List[Document], List[str], str]
    ) -> List[List[float]]:
        """Generates embeddings for the input text documents.

        Parameters
        ----------
        documents : Union[Documents, List[Document], List[str], str]
            The input text documents to generate embeddings for.

        Returns
        -------
        List[List[float]]
            The embeddings for the input text documents.
        """
        return self(documents)
