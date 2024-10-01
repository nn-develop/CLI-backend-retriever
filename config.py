import os

# Default values for backend
DEFAULT_GRPC_SERVER = os.getenv('GRPC_SERVER', 'localhost:50051')
DEFAULT_REST_URL = os.getenv('REST_URL', 'http://localhost:5000')

# Default output (stdout)
DEFAULT_OUTPUT = '-'

# Backend possible choices
BACKEND_GRPC = 'grpc'
BACKEND_REST = 'rest'
DEFAULT_SERVER_TYPE = BACKEND_REST
