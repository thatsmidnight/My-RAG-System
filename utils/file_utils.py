"""Utility functions for file operations."""
# Standard Library
import os
import logging
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_pdf_filepaths(base_folder: str) -> List[Optional[str]]:
    """Get all the filepaths of the pdf files in the base folder.

    Parameters
    ----------
    base_folder : str
        The base folder to search for pdf files.

    Returns
    -------
    List[Optional[str]]
        A list of filepaths of the pdf files in the base folder.
    """
    filepaths = []
    try:
        files = [
            f for f in os.listdir(base_folder)
            if os.path.isfile(os.path.join(base_folder, f))
        ]
        logger.info(
            "Found %s files in %s: %s" % (len(files), base_folder, files)
        )
        for file in files:
            if file.endswith(".pdf"):
                filepaths.append(os.path.join(base_folder, file))
    except OSError as e:
        logger.error("Error accessing %s: %s" % (base_folder, e))
    return filepaths
