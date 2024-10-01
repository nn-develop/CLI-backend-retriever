import requests
import unittest
from unittest.mock import patch
from rest_client import RestClient

class TestRestClient(unittest.TestCase):
    
    def setUp(self):
        self.client = RestClient('http://localhost:5000')  # Base URL is not used in tests

    @patch.object(RestClient, 'get_file_stat')
    def test_get_file_stat_valid_uuid(self, mock_get_file_stat):
        """Positive test: Should return file statistics for a valid UUID."""
        # Mock response for valid UUID
        mock_get_file_stat.return_value = {
            'name': 'example.txt',
            'size': 12345,
            'create_datetime': '2023-09-20T12:34:56Z',
            'mimetype': 'text/plain'
        }
        
        uuid = '1234-5678-9012-3456'  # Use a specific UUID for testing
        response = self.client.get_file_stat(uuid)
        
        # Verify that the response contains expected values
        self.assertIn('name', response)
        self.assertIn('size', response)
        self.assertIn('create_datetime', response)
        self.assertIn('mimetype', response)
        self.assertEqual(response['name'], 'example.txt')
        self.assertEqual(response['size'], 12345)

    @patch.object(RestClient, 'get_file_stat')
    def test_get_file_stat_invalid_uuid(self, mock_get_file_stat):
        """Negative test: Should raise FileNotFoundError for an invalid UUID."""
        # Mock response for an invalid UUID
        mock_get_file_stat.side_effect = FileNotFoundError("File with UUID invalid-uuid not found.")
        
        uuid = 'invalid-uuid'
        with self.assertRaises(FileNotFoundError) as context:
            self.client.get_file_stat(uuid)
        self.assertEqual(str(context.exception), f"File with UUID {uuid} not found.")

    @patch.object(RestClient, 'read_file')
    def test_read_file_valid_uuid(self, mock_read_file):
        """Positive test: Should return file content for a valid UUID."""
        # Mock response for valid UUID
        mock_read_file.return_value = ('example.txt', b'File content here.')
        
        uuid = '1234-5678-9012-3456'  # Specific UUID for testing
        file_name, file_content = self.client.read_file(uuid)
        
        # Verify that the response contains a file name and content
        self.assertEqual(file_name, 'example.txt')
        self.assertIsInstance(file_content, bytes)
        self.assertEqual(file_content, b'File content here.')

    @patch.object(RestClient, 'read_file')
    def test_read_file_invalid_uuid(self, mock_read_file):
        """Negative test: Should raise FileNotFoundError for an invalid UUID."""
        # Mock response for an invalid UUID
        mock_read_file.side_effect = FileNotFoundError("File with UUID invalid-uuid not found.")
        
        uuid = 'invalid-uuid'
        with self.assertRaises(FileNotFoundError) as context:
            self.client.read_file(uuid)
        self.assertEqual(str(context.exception), f"File with UUID {uuid} not found.")

    @patch.object(RestClient, 'get_file_stat')
    def test_get_file_stat_server_error(self, mock_get_file_stat):
        """Negative test: Should raise an exception for server errors (500)."""
        # Mock response for server error
        mock_get_file_stat.side_effect = requests.exceptions.HTTPError("500 Server Error")
        
        uuid = 'uuid-causing-server-error'
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.get_file_stat(uuid)

    @patch.object(RestClient, 'read_file')
    def test_read_file_server_error(self, mock_read_file):
        """Negative test: Should raise an exception for server errors (500)."""
        # Mock response for server error
        mock_read_file.side_effect = requests.exceptions.HTTPError("500 Server Error")
        
        uuid = 'uuid-causing-server-error'
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.read_file(uuid)

if __name__ == '__main__':
    unittest.main()
