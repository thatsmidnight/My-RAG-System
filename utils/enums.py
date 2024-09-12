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
GAME_SYSTEM_FOLDERS = [
    "Dragonbane",
    "Kids on Bikes 2e",
    "Star Wars 5e",
    "Risus The Anything RPG",
    "Gamma Wolves",
]
LOCAL_PATH_TO_TTRPG_PDFS = os.path.join(
    "..", "..", "Documents", "Tabletop RPGs"
)
PATH_TO_TTRPG_PDFS = "/app/data"
