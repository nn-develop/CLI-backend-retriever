import unittest
from unittest.mock import patch, Mock
import requests
from rest_client import RestClient

class TestRestClient(unittest.TestCase):

    def setUp(self) -> None:
        """
        Initialize the RestClient with a base URL for each test.
        """
        self.client = RestClient('http://localhost:5000')  # This URL will be mocked

    @patch('requests.get')
    def test_get_file_stat_valid_uuid(self, mock_get: Mock) -> None:
        """
        Positive test: Should return file statistics for a valid UUID.
        Mock the external request.get call to simulate a successful response.
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'example.txt',
            'size': 12345,
            'create_datetime': '2023-09-20T12:34:56Z',
            'mimetype': 'text/plain'
        }
        mock_get.return_value = mock_response

        uuid = '1234-5678-9012-3456'
        result = self.client.get_file_stat(uuid)

        self.assertEqual(result['name'], 'example.txt')
        self.assertEqual(result['size'], 12345)
        self.assertEqual(result['mimetype'], 'text/plain')
        mock_get.assert_called_once_with(f'http://localhost:5000/file/{uuid}/stat/')

    @patch('requests.get')
    def test_get_file_stat_file_not_found(self, mock_get: Mock) -> None:
        """
        Negative test: Should raise FileNotFoundError for an invalid UUID.
        Mock the external request.get call to simulate a 404 error.
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        uuid = 'invalid-uuid'
        with self.assertRaises(FileNotFoundError):
            self.client.get_file_stat(uuid)

        mock_get.assert_called_once_with(f'http://localhost:5000/file/{uuid}/stat/')

    @patch('requests.get')
    def test_get_file_stat_other_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server Error")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.get_file_stat("some-uuid")
        mock_get.assert_called_once_with("http://localhost:5000/file/some-uuid/stat/")

    @patch('requests.get')
    def test_read_file_valid_uuid(self, mock_get: Mock) -> None:
        """
        Positive test: Should return file content for a valid UUID.
        Mock the external request.get call to simulate a successful file read.
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Disposition': 'attachment; filename=example.txt'}
        mock_response.content = b'File content here.'
        mock_get.return_value = mock_response

        uuid = '1234-5678-9012-3456'
        file_name, file_content = self.client.read_file(uuid)

        self.assertEqual(file_name, 'example.txt')
        self.assertEqual(file_content, b'File content here.')
        mock_get.assert_called_once_with(f'http://localhost:5000/file/{uuid}/read/')

    @patch('requests.get')
    def test_read_file_file_not_found(self, mock_get: Mock) -> None:
        """
        Negative test: Should raise FileNotFoundError for an invalid UUID.
        Mock the external request.get call to simulate a 404 error.
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        uuid = 'invalid-uuid'
        with self.assertRaises(FileNotFoundError):
            self.client.read_file(uuid)

        mock_get.assert_called_once_with(f'http://localhost:5000/file/{uuid}/read/')

    @patch('requests.get')
    def test_read_file_server_error(self, mock_get: Mock) -> None:
        """
        Negative test: Should raise an HTTPError for a 500 server error.
        Mock the external request.get call to simulate a 500 error.
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server Error")
        mock_get.return_value = mock_response

        uuid = 'uuid-causing-server-error'
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.read_file(uuid)

        mock_get.assert_called_once_with(f'http://localhost:5000/file/{uuid}/read/')

if __name__ == '__main__':
    import unittest
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
