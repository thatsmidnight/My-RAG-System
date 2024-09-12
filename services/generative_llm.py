"""Module to define the GenerativeLLM class for generating text using Google's
Large Language Models.
"""

# Standard Library
from typing import Optional

# Third-Party
import google.generativeai as genai

# Local Folder
from utils.enums import LLM_MODEL


class GenerativeLLM:
    """Class to define the GenerativeModel for generating text using Google's
    Large Language Models.
    """

    @classmethod
    def get_model(
        cls, model_name: Optional[str] = LLM_MODEL
    ) -> genai.GenerativeModel:
        """Initializes the GenerativeModel instance with the specified model.

        Parameters
        ----------
        model_name : Optional[str], optional
            The name of the generative model to use, by default LLM_MODEL

        Returns
        -------
        genai.GenerativeModel
            The initialized GenerativeModel instance
        """
        return genai.GenerativeModel(model_name=model_name)
