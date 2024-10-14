import os
import sys
from concurrent import futures
import grpc
from google.protobuf.timestamp_pb2 import Timestamp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service_file_pb2 import *
from service_file_pb2_grpc import *
from server_grpc.file_data import FILES
import datetime

class FileServicer(FileServicer):
    """
    gRPC server for serving file metadata and content.
    """

    def stat(self, request, context):
        """
        Handle gRPC request for getting file metadata.
        """
        file_data = FILES.get(request.uuid.value)

        if file_data is None:
            # Pokud soubor neexistuje, vrátíme NOT_FOUND chybu
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")

        # Create a Timestamp object from the file's create_datetime
        timestamp = Timestamp()
        try:
            dt = datetime.datetime.fromisoformat(file_data["create_datetime"])
            timestamp.FromDatetime(dt)
        except ValueError:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid datetime format")

        return StatReply(
            data=StatReply.Data(
                name=file_data["name"],
                size=file_data["size"],
                create_datetime=timestamp,
                mimetype=file_data["mimetype"]
            )
        )

    def read(self, request, context):
        """
        Handle gRPC request for reading file content.
        """
        file_data = FILES.get(request.uuid.value)

        if file_data is None:
            # Pokud soubor neexistuje, vrátíme NOT_FOUND chybu
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")

        yield ReadReply(
            data=ReadReply.Data(
                data=file_data["content"]
            )
        )

def serve():
    """
    Start the gRPC server and listen for incoming connections.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_FileServicer_to_server(FileServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
