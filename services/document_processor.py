"""Module to process documents and extract text from them."""
# Standard Library
import re
import logging
from typing import List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Third-Party
import pymupdf
from pymupdf4llm import to_markdown

# Local Folder
from utils.file_utils import get_pdf_filepaths
from models.document import Document


class DocumentProcessor:
    """Class to process documents and extract text from them.
    """

    # Regular expression patterns to extract edition and title from the
    # filepath
    FOLDER_EDITION_PATTERN = r"([1-9]{1}[e]{1}$)"
    DOCUMENT_TITLE_PATTERN = r"(?<=- )(['\s\w]+)(?!-)"

    def __init__(self, base_folder: str) -> None:
        """Initialize a DocumentProcessor object with the specified base
        folder.

        Parameters
        ----------
        base_folder : str
            The base folder containing the documents to be processed.
        """
        self.base_folder = base_folder
        self.game_system = Path(self.base_folder).name
        self.edition = self._extract_edition()

    def _extract_edition(self) -> str:
        """Extract the edition of the game system from the base folder name.

        Returns
        -------
        str
            The extracted edition of the game system.
        """
        match = re.search(self.FOLDER_EDITION_PATTERN, self.base_folder)
        return match.group(1) if match else "1e"

    def _extract_title(self, filepath: str) -> str:
        """Extract the title of the document from the filepath.

        Parameters
        ----------
        filepath : str
            The filepath of the document. Expected format:
            `<base_folder>/Dragonbane - Bestiary - 20240607.pdf`
        Returns
        -------
        str
            The extracted title of the document.
        """
        match = re.search(self.DOCUMENT_TITLE_PATTERN, filepath)
        return match.group(1) if match else "1e"

    def process_documents(
        self, folder: Optional[str] = None
    ) -> Optional[List[Document]]:
        """Process the documents in the base folder and extract text from them.

        Parameters
        ----------
        folder : Optional[str], optional
            The folder containing the documents to be processed. If not
            specified, the base folder will be used, by default None.

        Returns
        -------
        Optional[List[Document]]
            A list of Document objects with text content extracted from the
            documents.
        """
        # Determine the folder to process
        folder = folder if folder else self.base_folder

        # Get the filepaths of the pdf files in the base folder
        logger.info(f"Processing documents in {folder}...")
        filepaths = get_pdf_filepaths(folder)
        documents = []

        # Check if any pdf files were found
        if filepaths == []:
            logger.error(f"No pdf files found in {folder}")
            return documents

        # Extract text content from each pdf file
        for filepath in filepaths:
            # Create a Document object and add it to the list
            logger.info(f"Extracting text from {filepath}...")
            title = self._extract_title(filepath=filepath)
            doc = pymupdf.open(filepath)
            document_pages = to_markdown(
                doc, pages=list(range(doc.page_count)), page_chunks=True
            )
            if type(document_pages) is str:
                document_pages = [document_pages]
            logger.info(
                f"Found {len(document_pages)} pages in {filepath}"
            )
            for idx, page_content in enumerate(document_pages):
                logger.debug(f"Extracting text from page {idx + 1}...")
                document = Document(
                    filepath=filepath,
                    page_content=page_content["text"],
                    title=title,
                    game_system=self.game_system,
                    edition=self.edition,
                    page_number=idx + 1,
                )
                documents.append(document)
                logger.debug(
                    f"Extracted text from {document.title} page "
                    f"{document.page_number}"
                )
            logger.info(
                f"Completed extracting {len(document_pages)} pages from "
                f"document in {filepath}"
            )

        return documents
