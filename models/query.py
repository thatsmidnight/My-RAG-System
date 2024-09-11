"""Module to define the Query class."""
from typing import Optional

from pydantic import BaseModel


class Query(BaseModel):
    """A Pydantic model representing a query text."""
    query: str
    top_k: Optional[int] = 15
