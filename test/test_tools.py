import json
import os
import unittest

from .tools import NumpyEncoder, sha3_512


class TestingToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.example_json_file = "assets/test/json_example.json"
        with open(self.example_json_file) as fin:
            self.example_json_data = json.load(fin)

        self.test_json_file = "json_example.json"

        return super().setUp()

    def test_numpy_encoder(self):
        with open(self.test_json_file, "w") as fin:
            json.dump(self.example_json_data, fin, indent=2, cls=NumpyEncoder)
        self.assertEqual(
            sha3_512(self.example_json_file), sha3_512(self.test_json_file)
        )

    def tearDown(self):
        if os.path.isfile(self.test_json_file):
            os.remove(self.test_json_file)

        return super().tearDown()
