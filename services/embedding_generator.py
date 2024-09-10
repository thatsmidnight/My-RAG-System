"""This module contains the EmbeddingGenerator class, which generates
embeddings for text documents using Google's Text Embedding API and stores
them in a ChromaDB collection.
"""
import logging
from typing import List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from chromadb import EmbeddingFunction, Documents

from models.document import Document
from utils import enums
from services.embedding_function import GeminiEmbeddingFunction


class EmbeddingGenerator:
    """Generates embeddings for text documents using Google's Text Embedding
    API and stores them in a ChromaDB collection.
    """

    def __init__(
        self,
        embedding_function: Optional[EmbeddingFunction] = None,
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
        """
        self.embedding_function = (
            embedding_function or GeminiEmbeddingFunction(
                model=model_name, output_dimensionality=output_dimensionality
            )
        )

    def _chunkify_text(
        self, text: str,
        chunk_size: Optional[int] = 1000,
        chunk_overlap: Optional[int] = 100
    ) -> List[str]:
        """Splits a text into chunks of a specified size with a specified
        overlap.

        Parameters
        ----------
        text : str
            The text to split into chunks.
        chunk_size : Optional[int], optional
            The size of each text chunk, by default 1000.
        chunk_overlap : Optional[int], optional
            The overlap between chunks, by default 100.

        Returns
        -------
        List[str]
            A list of text chunks.
        """
        # Initialize variables
        chunks = []
        start = 0
        end = chunk_size
        chunk_overlap = (
            0 if chunk_overlap is None or chunk_overlap < 0 else chunk_overlap
        )

        # Split the text into chunks
        while start < len(text):
            chunks.append(text[start:end])
            start = end - chunk_overlap
            end = start + chunk_size

        return chunks

    def generate_embeddings(
        self,
        documents: Union[Documents, List[Document], List[str], str],
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = 100,
    ) -> None:
        """Generates embeddings for the input text documents.

        Parameters
        ----------
        documents : Union[Documents, List[Document], List[str], str]
            The input text documents to generate embeddings for.
        chunk_size : Optional[int], optional
            The size of each text chunk, by default None.
        chunk_overlap : Optional[int], optional
            The overlap between chunks, by default 100.
        """
        # Convert input to a list of strings
        if isinstance(documents, str):
            documents = [documents]
        elif (
            isinstance(documents, list)
            and len(documents) > 0
            and isinstance(documents[0], Document)
        ):
            documents = [doc.page_content for doc in documents]

        # Get chunks of text if chunk_size is specified
        if chunk_size is not None and chunk_size > 0 and chunk_overlap > 0:
            logger.info(
                "Chunking text into chunks of size %s with an overlap of %s..."
                % (chunk_size, chunk_overlap)
            )
            documents = [
                self._chunkify_text(doc, chunk_size, chunk_overlap)
                for doc in documents
            ]

        # Generate embeddings for the input text documents
        logger.info(
            "Generating embeddings for %s documents..." % (len(documents))
        )
        if len(documents) > 0:
            return self.embedding_function(documents)
        else:
            return []
