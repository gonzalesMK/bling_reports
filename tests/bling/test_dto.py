from unittest import TestCase
from pathlib import Path
import json

from reports.bling.dto import GetSales

TEST_FOLDER = Path(__file__).parent.parent / "resources"


class TestDTO(TestCase):
    def test_dto_dont_throw(self):
        GetSales.parse_file(TEST_FOLDER / "example_list_sales_response.json")

    def test_dto_no_resource_found(self):
        GetSales.parse_file(TEST_FOLDER / "bling_no_resource_found.json")
