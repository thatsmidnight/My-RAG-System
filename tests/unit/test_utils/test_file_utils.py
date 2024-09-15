import os
import unittest
from unittest import mock
from utils import file_utils


class TestFileUtils(unittest.TestCase):

    def test_get_pdf_filepaths(self):
        """Test the get_pdf_filepaths function.
        """
        # Test the function
        filepaths = file_utils.get_pdf_filepaths(os.path.join("tests", "data"))
        assert len(filepaths) == 2
        assert filepaths[0] == os.path.join("tests", "data", "test1.pdf")
        assert filepaths[1] == os.path.join("tests", "data", "test2.pdf")

    def test_get_pdf_filepaths_error(self):
        """Test the get_pdf_filepaths function with an error.
        """
        # Mock the os.listdir function to raise an OSError
        with mock.patch("os.listdir") as mock_listdir:
            mock_listdir.side_effect = OSError("test")
            filepaths = file_utils.get_pdf_filepaths(
                os.path.join("tests", "data")
            )
            assert len(filepaths) == 0

    def test_get_pdf_filepaths_empty_list(self):
        """Test the get_pdf_filepaths function.
        """
        # Test the function
        filepaths = file_utils.get_pdf_filepaths(
            os.path.join("tests", "data2")
        )
        assert len(filepaths) == 0
