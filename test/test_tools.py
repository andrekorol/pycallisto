import json
import unittest
from pathlib import Path

from .tools import NumpyEncoder, sha3_512


class TestingToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.example_json_file = "assets/test/json_example.json"
        with open(self.example_json_file) as fin:
            self.example_json_data = json.load(fin)

        self.test_json_file = Path("json_example.json")

        return super().setUp()

    def test_numpy_encoder(self):
        with open(self.test_json_file, "w") as fin:
            json.dump(self.example_json_data, fin, indent=2, cls=NumpyEncoder)
        self.assertEqual(
            sha3_512(self.example_json_file), sha3_512(self.test_json_file)
        )

    def tearDown(self):
        self.test_json_file.unlink(missing_ok=True)

        return super().tearDown()
