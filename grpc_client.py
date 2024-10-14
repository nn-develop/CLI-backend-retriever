import grpc
import service_file_pb2
import service_file_pb2_grpc

class GrpcClient:
    """
    Client for interacting with the gRPC backend.
    """

    def __init__(self, server_address):
        """
        Initialize the gRPC client with the server address.

        :param server_address: Address of the gRPC server.
        """
        self.server_address = server_address
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = service_file_pb2_grpc.FileStub(self.channel)  # Corrected to FileStub

    def get_file_stat(self, uuid):
        """
        Get file metadata from the server.

        :param uuid: UUID of the file.
        :return: File metadata.
        """
        request = service_file_pb2.StatRequest(uuid=service_file_pb2.Uuid(value=uuid))
        response = self.stub.stat(request)
        return {
            'name': response.data.name,
            'size': response.data.size,
            'create_datetime': response.data.create_datetime,
            'mimetype': response.data.mimetype
        }

    def read_file(self, uuid):
        """
        Read file content from the server.

        :param uuid: UUID of the file.
        :return: File name and file content.
        """
        request = service_file_pb2.ReadRequest(uuid=service_file_pb2.Uuid(value=uuid))
        response = self.stub.read(request)
        for file_chunk in response:
            return file_chunk.data.data
