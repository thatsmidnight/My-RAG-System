# Global variables
global VECTOR_STORE_PATH
VECTOR_STORE_PATH = None
global LAST_UPDATE_TIME
LAST_UPDATE_TIME = 0

# Static variables
PDF_FOLDER_PATH = "pdfs"
VECTOR_STORE_PATH = "vector_store"
EMBEDDING_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-1.5-flash"
LANGCHAIN_OWNER_REPO_COMMIT = "rlm/rag-prompt"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
