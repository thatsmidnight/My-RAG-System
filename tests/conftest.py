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
            "python-dotenv is not installed. Environment variables must be set "
            "manually."
        )
    PATH_TO_TTRPG_PDFS = enums.LOCAL_PATH_TO_TTRPG_PDFS
else:
    PATH_TO_TTRPG_PDFS = enums.PATH_TO_TTRPG_PDFS
