"""Module to define the ChromaDB class."""
from typing import Optional

from chromadb import EmbeddingFunction, PersistentClient
from chromadb.config import Settings

from utils import enums
from services.embedding_function import GeminiEmbeddingFunction


class ChromaDB:

    def __init__(
        self,
        embedding_function: Optional[EmbeddingFunction] = None,
        chroma_db_path: Optional[str] = enums.CHROMA_DB_PATH,
        collection_name: Optional[str] = enums.COLLECTION_NAME,
        settings: Optional[Settings] = None
    ) -> None:
        if not embedding_function:
            self.embedding_function = GeminiEmbeddingFunction(
                model=enums.EMBEDDING_MODEL,
                output_dimensionality=enums.OUTPUT_DIMENSIONALITY,
            )

        if not settings:
            self.settings = Settings(anonymized_telemetry=False)
        else:
            self.settings = settings

        self.chroma_client = PersistentClient(
            path=chroma_db_path,
            settings=self.settings,
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name=enums.COLLECTION_NAME, embedding_function=embedding_function
        )
