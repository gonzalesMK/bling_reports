from unittest import TestCase
from pathlib import Path
import json

from reports.bling.dto import GetSales

TEST_FOLDER = Path(__file__).parent


class TestDTO(TestCase):
    def test_dto_dont_throw(self):
        GetSales.parse_file(TEST_FOLDER / "example_list_sales_response.json")
