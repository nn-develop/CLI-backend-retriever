# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import service_file_pb2 as service__file__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in service_file_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class FileStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.stat = channel.unary_unary(
                '/File/stat',
                request_serializer=service__file__pb2.StatRequest.SerializeToString,
                response_deserializer=service__file__pb2.StatReply.FromString,
                _registered_method=True)
        self.read = channel.unary_stream(
                '/File/read',
                request_serializer=service__file__pb2.ReadRequest.SerializeToString,
                response_deserializer=service__file__pb2.ReadReply.FromString,
                _registered_method=True)


class FileServicer(object):
    """Missing associated documentation comment in .proto file."""

    def stat(self, request, context):
        """Get file metadata

        * Return INVALID_ARGUMENT if invalid UUID is used.
        * Return NOT_FOUND if file is not found.
        * Return FAILED_PRECONDITION in case of database errors.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def read(self, request, context):
        """Read file content

        * Return INVALID_ARGUMENT if invalid UUID is used.
        * Return NOT_FOUND if file is not found.
        * Return FAILED_PRECONDITION in case of database or file system errors.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=service__file__pb2.StatRequest.FromString,
                    response_serializer=service__file__pb2.StatReply.SerializeToString,
            ),
            'read': grpc.unary_stream_rpc_method_handler(
                    servicer.read,
                    request_deserializer=service__file__pb2.ReadRequest.FromString,
                    response_serializer=service__file__pb2.ReadReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'File', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('File', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class File(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/File/stat',
            service__file__pb2.StatRequest.SerializeToString,
            service__file__pb2.StatReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/File/read',
            service__file__pb2.ReadRequest.SerializeToString,
            service__file__pb2.ReadReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
