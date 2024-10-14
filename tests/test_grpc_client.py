import unittest
from unittest.mock import patch, MagicMock
from grpc_client import GrpcClient
from service_file_pb2 import StatReply, ReadReply, Uuid
from google.protobuf.timestamp_pb2 import Timestamp
from grpc import StatusCode
import grpc


class TestGrpcClient(unittest.TestCase):

    def setUp(self):
        """Set up the GrpcClient for each test."""
        self.client = GrpcClient(server_address="localhost:50051")

    @patch('grpc.insecure_channel')
    @patch('service_file_pb2_grpc.FileStub')
    def test_get_file_stat_success(self, mock_stub, mock_channel):
        """Positive test: Should return file metadata for a valid UUID."""
        mock_stub.return_value.stat.return_value = StatReply(
            data=StatReply.Data(
                name="example.txt",
                size=1024,
                create_datetime=Timestamp(seconds=1600000000),
                mimetype="text/plain"
            )
        )

        uuid = "123e4567-e89b-12d3-a456-426614174000"
        response = self.client.get_file_stat(uuid)

        self.assertEqual(response['name'], "example.txt")
        self.assertEqual(response['size'], 1024)
        self.assertEqual(response['mimetype'], "text/plain")

    @patch('grpc.insecure_channel')
    @patch('service_file_pb2_grpc.FileStub')
    def test_get_file_stat_not_found(self, mock_stub, mock_channel):
        """Negative test: Should raise FileNotFoundError for an invalid UUID."""
        mock_stub.return_value.stat.side_effect = grpc.RpcError(StatusCode.NOT_FOUND)

        uuid = "invalid_uuid"
        with self.assertRaises(grpc.RpcError) as context:
            self.client.get_file_stat(uuid)
        self.assertEqual(context.exception.code(), StatusCode.NOT_FOUND)

    @patch('grpc.insecure_channel')
    @patch('service_file_pb2_grpc.FileStub')
    def test_read_file_success(self, mock_stub, mock_channel):
        """Positive test: Should return file content for a valid UUID."""
        mock_stub.return_value.read.return_value = iter([
            ReadReply(data=ReadReply.Data(data=b"Hello, this is an example file content."))
        ])

        uuid = "123e4567-e89b-12d3-a456-426614174000"
        response = self.client.read_file(uuid)

        self.assertEqual(response, b"Hello, this is an example file content.")

    @patch('grpc.insecure_channel')
    @patch('service_file_pb2_grpc.FileStub')
    def test_read_file_not_found(self, mock_stub, mock_channel):
        """Negative test: Should raise FileNotFoundError for an invalid UUID."""
        mock_stub.return_value.read.side_effect = grpc.RpcError(StatusCode.NOT_FOUND)

        uuid = "invalid_uuid"
        with self.assertRaises(grpc.RpcError) as context:
            self.client.read_file(uuid)
        self.assertEqual(context.exception.code(), StatusCode.NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
