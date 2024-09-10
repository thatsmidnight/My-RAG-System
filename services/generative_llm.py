"""Module to define the GenerativeLLM class for generating text using Google's
Large Language Models.
"""

from typing import Optional

import google.generativeai as genai

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
