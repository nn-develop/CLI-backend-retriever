import os
import sys
import unittest
from unittest.mock import patch
from grpc import StatusCode, RpcError
from google.protobuf.timestamp_pb2 import Timestamp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service_file_pb2 import *
from server_grpc.grpc_server import FileServicer
from server_grpc.file_data import FILES


class TestGrpcServer(unittest.TestCase):

    def setUp(self):
        """Set up the gRPC server servicer instance for each test."""
        self.servicer = FileServicer()

    @patch('server_grpc.file_data.FILES', {
        "123e4567-e89b-12d3-a456-426614174000": {
            "name": "example.txt",
            "size": 1024,
            "create_datetime": "2023-09-20T12:34:56",
            "mimetype": "text/plain",
            "content": b"File content here."
        }
    })
    def test_stat_success(self):
        """Positive test: Should return file metadata for a valid UUID."""
        request = StatRequest(uuid=Uuid(value="123e4567-e89b-12d3-a456-426614174000"))
        context = unittest.mock.Mock()

        response = self.servicer.stat(request, context)

        self.assertIsInstance(response, StatReply)
        self.assertEqual(response.data.name, "example.txt")
        self.assertEqual(response.data.size, 1024)
        self.assertEqual(response.data.mimetype, "text/plain")

    @patch('server_grpc.file_data.FILES', {})
    def test_stat_not_found(self):
        """Negative test: Should return NOT_FOUND for an invalid UUID."""
        request = StatRequest(uuid=Uuid(value="invalid_uuid"))
        context = unittest.mock.Mock()

        with self.assertRaises(RpcError) as context_manager:
            self.servicer.stat(request, context)

        self.assertEqual(context_manager.exception.code(), StatusCode.NOT_FOUND)

    @patch('server_grpc.file_data.FILES', {
        "123e4567-e89b-12d3-a456-426614174000": {
            "name": "example.txt",
            "size": 1024,
            "create_datetime": "2023-09-20T12:34:56",
            "mimetype": "text/plain",
            "content": b"File content here."
        }
    })
    def test_read_success(self):
        """Positive test: Should return file content for a valid UUID."""
        request = ReadRequest(uuid=Uuid(value="123e4567-e89b-12d3-a456-426614174000"))
        context = unittest.mock.Mock()

        response = list(self.servicer.read(request, context))
        self.assertIsInstance(response[0], ReadReply)
        self.assertEqual(response[0].data.data, b"Hello, this is an example file content.")

    @patch('server_grpc.file_data.FILES', {})
    def test_read_not_found(self):
        """Negative test: Should return NOT_FOUND for an invalid UUID."""
        request = ReadRequest(uuid=Uuid(value="invalid_uuid"))
        context = unittest.mock.Mock()

        with self.assertRaises(RpcError) as context_manager:
            list(self.servicer.read(request, context))

        self.assertEqual(context_manager.exception.code(), StatusCode.NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
