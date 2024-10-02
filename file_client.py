#!/usr/bin/env python3
import sys
import argparse
from rest_client import RestClient
# from grpc_client import GrpcClient
from config import BACKEND_REST, BACKEND_GRPC, DEFAULT_REST_URL, DEFAULT_GRPC_SERVER, DEFAULT_SERVER_TYPE, DEFAULT_OUTPUT

class FileClient:
    def __init__(self, backend, rest_base_url=None, grpc_server=None, output=None):
        """Initialize FileClient with backend and configurations."""
        self.backend = backend
        self.output = output or DEFAULT_OUTPUT
        
        if self.backend == BACKEND_REST:
            self.client = RestClient(base_url=rest_base_url or DEFAULT_REST_URL)
        # elif self.backend == BACKEND_GRPC:
        #     self.client = GrpcClient(server_address=grpc_server or DEFAULT_GRPC_SERVER)
        else:
            raise ValueError(f"Unknown backend: {self.backend}")

    def stat(self, uuid):
        """Retrieve and print file metadata."""
        stat_data = self.client.get_file_stat(uuid)
        self._print_stat(stat_data)

    def read(self, uuid):
        """Read file content by UUID."""
        file_name, file_content = self.client.read_file(uuid)
        self._write_output(file_content, file_name)

    def _print_stat(self, stat_data):
        """Print file metadata to console."""
        print(f"Name: {stat_data['name']}")
        print(f"Size: {stat_data['size']} bytes")
        print(f"Created: {stat_data['create_datetime']}")
        print(f"MIME Type: {stat_data['mimetype']}")

    def _write_output(self, content, file_name):
        """Write file content to the specified output."""
        if self.output == '-':
            sys.stdout.buffer.write(content)
        else:
            with open(self.output, 'wb') as f:
                f.write(content)

def main():
    """Main function for parsing arguments and executing commands."""
    parser = argparse.ArgumentParser(
        description='CLI client to interact with REST or gRPC server.\n'
                    'Usage: file-client [options] stat UUID\n'
                    '       file-client [options] read UUID\n'
                    '       file-client --help',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('command', choices=['stat', 'read'],
                        help='Command to execute:\n'
                             'stat - Prints the file metadata in a human-readable manner.\n'
                             'read - Outputs the file content.')
    parser.add_argument('uuid', help='UUID of the file')
    parser.add_argument('--backend', choices=[BACKEND_GRPC, BACKEND_REST],
                        default=DEFAULT_SERVER_TYPE,
                        help=f'Backend to use (default: {DEFAULT_SERVER_TYPE})')
    parser.add_argument('--base-url',
                        default=DEFAULT_REST_URL, 
                        help=f'Base URL for REST server (default: {DEFAULT_REST_URL})')
    parser.add_argument('--grpc-server',
                        default=DEFAULT_GRPC_SERVER, 
                        help=f'Host and port of the gRPC server (default: {DEFAULT_GRPC_SERVER})')
    parser.add_argument('--output',
                        default=DEFAULT_OUTPUT,
                        help=f'Set the output file (default: {DEFAULT_OUTPUT})')

    args = parser.parse_args()

    """Initialize FileClient and execute the given command."""
    client = FileClient(
        backend=args.backend,
        rest_base_url=args.base_url,
        grpc_server=args.grpc_server,
        output=args.output
    )

    if args.command == "stat":
        client.stat(args.uuid)
    elif args.command == "read":
        client.read(args.uuid)

if __name__ == "__main__":
    main()
