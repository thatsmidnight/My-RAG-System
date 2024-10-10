"""Pytest configuration file.
"""

# Standard Library
import os
import logging

import pytest

from utils import enums

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Static variables
IS_LOCAL = os.getenv("IS_LOCAL")
if IS_LOCAL:
    try:
        # Third-Party
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        logger.warning(
            "python-dotenv is not installed. Environment variables must be "
            "set manually."
        )
    PATH_TO_PDFS = enums.PATH_TO_FOLDERS
else:
    PATH_TO_PDFS = enums.PATH_TO_PDFS


# Fixtures
@pytest.fixture(scope="session")
def path_to_ttrpg_pdfs():
    """Fixture to provide the path to TTRPG PDFs."""
    return PATH_TO_PDFS


@pytest.fixture(scope="session")
def embedding_model():
    """Fixture to provide the embedding model."""
    return enums.EMBEDDING_MODEL


@pytest.fixture(scope="session")
def llm_model():
    """Fixture to provide the LLM model."""
    return enums.LLM_MODEL


@pytest.fixture(scope="session")
def chroma_db_path():
    """Fixture to provide the ChromaDB path."""
    return enums.CHROMA_DB_PATH


@pytest.fixture(scope="session")
def collection_name():
    """Fixture to provide the collection name."""
    return enums.COLLECTION_NAME


@pytest.fixture(scope="session")
def FOLDER_CONTAINING_FILES():
    """Fixture to provide the game system folders."""
    return enums.FOLDER_CONTAINING_FILES
