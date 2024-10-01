import os
import sys
import unittest
from flask import Flask
from flask_server.server import app, FileMetadata, FileService, FileAPI

class FileAPITestCase(unittest.TestCase):

    def setUp(self):
        """Set up the Flask test client and initialize services for each test."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_file_path = os.path.join(current_dir, "example.txt")

        with open(self.test_file_path, "w") as f:
            f.write("This is a test file.")

        # Custom test data with an existing file path for successful tests
        self.file_service = FileService(files_metadata={
            "1234": FileMetadata(
                uuid="1234",
                create_datetime="2023-09-20T12:34:56Z",
                size=12345,
                mimetype="text/plain",
                name="example.txt",
                path=self.test_file_path
            )
        })

        # Create a new Flask app instance for each test to avoid route conflicts
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()
        self.file_api = FileAPI(self.app, self.file_service)

    def tearDown(self):
        """Clean up the test environment after each test."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_file_stat_success(self):
        """Test file stat endpoint with a valid UUID."""
        response = self.client.get('/file/1234/stat/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("create_datetime", response.json)
        self.assertIn("size", response.json)
        self.assertIn("mimetype", response.json)
        self.assertIn("name", response.json)

    def test_file_stat_not_found(self):
        """Test file stat endpoint with an invalid UUID."""
        response = self.client.get('/file/invalid_uuid/stat/')
        self.assertEqual(response.status_code, 404)
        self.assertIn("File with UUID invalid_uuid not found.", response.get_data(as_text=True))

    def test_read_file_success(self):
        """Test file read endpoint with a valid UUID."""
        response = self.client.get('/file/1234/read/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers['Content-Type'].startswith('text/plain'))
        self.assertIn('Content-Disposition', response.headers)

    def test_read_file_not_found(self):
        """Test file read endpoint with an invalid UUID."""
        response = self.client.get('/file/invalid_uuid/read/')
        self.assertEqual(response.status_code, 404)
        self.assertIn("File with UUID invalid_uuid not found.", response.get_data(as_text=True))

    def test_file_stat_missing_parameter(self):
        """Test file stat endpoint with missing UUID parameter."""
        response = self.client.get('/file//stat/')
        self.assertEqual(response.status_code, 404)

    def test_read_file_missing_file(self):
        """Test read file endpoint with a valid UUID but missing file on disk."""
        self.file_service.files_metadata["1234"].path = "non_existing_path.txt"
        response = self.client.get('/file/1234/read/')
        self.assertEqual(response.status_code, 404)
        self.assertIn("File with UUID 1234 not found.", response.get_data(as_text=True))

    def test_file_stat_invalid_uuid_format(self):
        """Test file stat endpoint with a malformed UUID."""
        response = self.client.get('/file/!!invalid_uuid_format!!/stat/')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
