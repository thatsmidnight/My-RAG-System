"""Module to define the Document class."""
# Standard Library
from uuid import uuid4
from typing import Optional, Union, List


class Document:
    """Class to represent a document object.
    """
    @property
    def filepath(self) -> str:
        """The filepath of the document."""
        return self.metadata["filepath"]

    @property
    def title(self) -> str:
        """The title of the document."""
        return self.metadata["title"]

    @property
    def game_system(self) -> str:
        """The game system associated with the document."""
        return self.metadata["game_system"]

    @property
    def edition(self) -> str:
        """The edition of the game system."""
        return self.metadata["edition"]

    @property
    def page_number(self) -> int:
        """The page number of the document."""
        return self.metadata["page_number"]

    def __init__(
        self,
        filepath: str,
        page_content: Union[str, List[str]],
        title: str,
        game_system: str,
        edition: Optional[str] = "1e",
        page_number: int = 1,
    ) -> None:
        """Initialize a Document object with the specified attributes.

        Parameters
        ----------
        filepath : str
            The filepath of the document.
        page_content : Union[str, List[str]]
            The content of the document.
        title : str
            The title of the document.
        game_system : str
            The game system associated with the document.
        edition : Optional[str], optional
            The edition of the game system, by default "1e".
        page_number : int, optional
            The page number of the document, by default 1.
        """
        self.page_content = page_content
        self.id = str(uuid4())
        self.metadata = {
            "title": title,
            "game_system": game_system,
            "edition": edition,
            "filepath": filepath,
            "page_number": page_number,
        }
