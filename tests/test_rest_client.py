import unittest
import responses
from rest_client import RestClient
import requests

class TestRestClient(unittest.TestCase):

    def setUp(self) -> None:
        """
        Initialize the RestClient with a base URL for each test.
        """
        self.client = RestClient('http://localhost:5000')

    @responses.activate
    def test_get_file_stat_valid_uuid(self) -> None:
        """
        Positive test: Should return file statistics for a valid UUID.
        Use `responses` to mock the external request.
        """
        uuid = '1234-5678-9012-3456'
        responses.add(
            responses.GET,
            f'http://localhost:5000/file/{uuid}/stat/',
            json={
                'name': 'example.txt',
                'size': 12345,
                'create_datetime': '2023-09-20T12:34:56Z',
                'mimetype': 'text/plain'
            },
            status=200
        )

        result = self.client.get_file_stat(uuid)

        self.assertEqual(result['name'], 'example.txt')
        self.assertEqual(result['size'], 12345)
        self.assertEqual(result['mimetype'], 'text/plain')

    @responses.activate
    def test_get_file_stat_file_not_found(self) -> None:
        """
        Negative test: Should raise FileNotFoundError for an invalid UUID.
        Use `responses` to mock a 404 error.
        """
        uuid = 'invalid-uuid'
        responses.add(
            responses.GET,
            f'http://localhost:5000/file/{uuid}/stat/',
            status=404
        )

        with self.assertRaises(FileNotFoundError):
            self.client.get_file_stat(uuid)

    @responses.activate
    def test_get_file_stat_other_error(self) -> None:
        """
        Test handling of a server error (500).
        """
        uuid = 'some-uuid'
        responses.add(
            responses.GET,
            f'http://localhost:5000/file/{uuid}/stat/',
            status=500
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.get_file_stat(uuid)

    @responses.activate
    def test_read_file_valid_uuid(self) -> None:
        """
        Positive test: Should return file content for a valid UUID.
        Use `responses` to mock the external request.
        """
        uuid = '1234-5678-9012-3456'
        responses.add(
            responses.GET,
            f'http://localhost:5000/file/{uuid}/read/',
            headers={'Content-Disposition': 'attachment; filename=example.txt'},
            body=b'File content here.',
            status=200
        )

        file_name, file_content = self.client.read_file(uuid)

        self.assertEqual(file_name, 'example.txt')
        self.assertEqual(file_content, b'File content here.')

    @responses.activate
    def test_read_file_file_not_found(self) -> None:
        """
        Negative test: Should raise FileNotFoundError for an invalid UUID.
        Use `responses` to mock a 404 error.
        """
        uuid = 'invalid-uuid'
        responses.add(
            responses.GET,
            f'http://localhost:5000/file/{uuid}/read/',
            status=404
        )

        with self.assertRaises(FileNotFoundError):
            self.client.read_file(uuid)

    @responses.activate
    def test_read_file_server_error(self) -> None:
        """
        Negative test: Should raise an HTTPError for a 500 server error.
        Use `responses` to mock a 500 error.
        """
        uuid = 'uuid-causing-server-error'
        responses.add(
            responses.GET,
            f'http://localhost:5000/file/{uuid}/read/',
            status=500
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.read_file(uuid)


if __name__ == '__main__':
    import unittest
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
