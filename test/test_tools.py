import asyncio
import json
import unittest
from pathlib import Path

from .tools import NumpyEncoder, download_file, sha3_512


class NumpyEncoderTestCase(unittest.TestCase):
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


class DownloadFileTestCase(unittest.TestCase):
    def setUp(self):
        self.original_sales_records = "assets/test/1500000 Sales Records.7z"
        sales_records_url = (
            "http://eforexcel.com/wp/wp-content/uploads/2017/07/"
            "1500000%20Sales%20Records.7z"
        )
        self.test_sales_records = asyncio.run(download_file(sales_records_url))

        self.original_faces_dataset = "assets/test/All-Age-Faces Dataset.zip"
        faces_dataset_url = (
            "https://www.dropbox.com/s/a0lj1ddd54ns8qy/"
            "All-Age-Faces%20Dataset.zip?dl=1"
        )
        self.test_faces_dataset = asyncio.run(download_file(faces_dataset_url))

        return super().setUp()

    def test_download_file(self):
        self.assertEqual(
            sha3_512(self.original_sales_records), sha3_512(self.test_sales_records)
        )

        self.assertEqual(
            sha3_512(self.original_faces_dataset), sha3_512(self.test_faces_dataset)
        )

    def tearDown(self):
        self.test_sales_records.unlink(missing_ok=True)
        self.test_faces_dataset.unlink(missing_ok=True)

        return super().tearDown()
