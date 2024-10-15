from io import StringIO
import unittest
from unittest.mock import patch, mock_open, Mock
from file_client import FileClient

class TestFileClient(unittest.TestCase):
    
    def setUp(self) -> None:
        self.client: FileClient = FileClient(backend='rest', output='output.txt')

    @patch('builtins.print')
    def test_print_stat(self, mock_print: Mock) -> None:
        """Positive test: Should correctly print file statistics."""
        stat_data: dict = {
            'name': 'example.txt',
            'size': 12345,
            'create_datetime': '2023-09-20T12:34:56Z',
            'mimetype': 'text/plain'
        }

        self.client._print_stat(stat_data)

        mock_print.assert_any_call("Name: example.txt")
        mock_print.assert_any_call("Size: 12345 bytes")
        mock_print.assert_any_call("Created: 2023-09-20T12:34:56Z")
        mock_print.assert_any_call("MIME Type: text/plain")

    @patch('builtins.open', new_callable=mock_open)
    def test_write_output_to_file(self, mock_file: Mock) -> None:
        """Positive test: Should correctly write content to a file."""
        file_name: str = 'output.txt'
        file_content: bytes = b'File content here.'

        self.client._write_output(file_content, file_name)

        mock_file.assert_called_once_with('output.txt', 'wb')
        mock_file().write.assert_called_once_with(file_content)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_output_to_stdout(self, mock_file: Mock) -> None:
        """Positive test: Should correctly write content to stdout."""
        self.client.output = '-'
        file_name: str = 'example.txt'
        file_content: bytes = b'File content here.'

        self.client._write_output(file_content, file_name)
        mock_file.assert_not_called()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.client._write_output(file_content, file_name)
            expected_output: str = file_content.decode('utf-8', errors='replace')
            self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
