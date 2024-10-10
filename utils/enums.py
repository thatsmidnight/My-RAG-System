"""Enums for the project."""

# Standard Library
import os.path

# Global variables
global VECTOR_STORE
VECTOR_STORE = None

# Static variables
COLLECTION_NAME = "ttrpg_documents"
CHROMA_DB_PATH = "chroma_db"
EMBEDDING_MODEL = "models/text-embedding-004"
OUTPUT_DIMENSIONALITY = 768
LLM_MODEL = "models/gemini-1.5-pro"
LANGCHAIN_OWNER_REPO_COMMIT = "rlm/rag-prompt"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Local folders
FOLDER_CONTAINING_FILES = ["Ableton v12"]
PATH_TO_FOLDERS = os.path.join("..", "..", "Documents", "Documentation")
PATH_TO_PDFS = "/app/data"
