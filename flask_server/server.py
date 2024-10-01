from flask import Flask, jsonify, send_file, abort, after_this_request
import os
import logging

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up logging
logging.basicConfig(level=logging.INFO)

class FileMetadata:
    """Class representing the metadata of a file."""
    
    def __init__(self, uuid, create_datetime, size, mimetype, name, path):
        self.uuid = uuid
        self.create_datetime = create_datetime
        self.size = size
        self.mimetype = mimetype
        self.name = name
        self.path = path

    def to_dict(self) -> dict:
        """Return the metadata of the file as a dictionary."""
        return {
            "create_datetime": self.create_datetime,
            "size": self.size,
            "mimetype": self.mimetype,
            "name": self.name
        }

class FileService:
    """Class providing services for managing files."""
    
    def __init__(self, files_metadata: dict = None):
        self.files_metadata = files_metadata or {}

    def add_file_metadata(self, file_metadata: FileMetadata) -> None:
        """Add a new file's metadata."""
        self.files_metadata[file_metadata.uuid] = file_metadata

    def delete_file_metadata(self, uuid: str) -> None:
        """Delete a file's metadata by its UUID."""
        self.files_metadata.pop(uuid, None)

    def get_file_metadata(self, uuid: str) -> FileMetadata:
        """Return the metadata of a file by its UUID."""
        return self.files_metadata.get(uuid)

    def file_exists(self, uuid: str) -> bool:
        """Check if the file exists by its UUID."""
        file_data = self.get_file_metadata(uuid)
        return file_data and os.path.exists(file_data.path)

class FileAPI:
    """Class that handles API routes for file operations."""

    def __init__(self, app: Flask, file_service: FileService):
        self.app = app
        self.file_service = file_service
        self.register_routes()

    def register_routes(self) -> None:
        """Register all the API endpoints."""
        self.app.add_url_rule('/file/<uuid>/stat/', view_func=self.file_stat, methods=['GET'])
        self.app.add_url_rule('/file/<uuid>/read/', view_func=self.read_file, methods=['GET'])

    def file_stat(self, uuid: str):
        """Endpoint for retrieving the metadata of a file."""
        file_data = self.file_service.get_file_metadata(uuid)
        
        if file_data:
            return jsonify(file_data.to_dict())
        else:
            logging.error(f"File with UUID {uuid} not found.")
            abort(404, description=f"File with UUID {uuid} not found.")

    def read_file(self, uuid: str):
        """Endpoint for reading the content of a file."""
        file_data = self.file_service.get_file_metadata(uuid)
        
        if file_data:
            if not os.path.exists(file_data.path):
                logging.error(f"File with UUID {uuid} not found on disk.")
                abort(404, description=f"File with UUID {uuid} not found.")

            @after_this_request
            def close_file(response):
                try:
                    response.direct_passthrough = False
                    response.stream.close()
                except Exception as e:
                    logging.exception("Error closing file stream.")
                return response

            return send_file(
                file_data.path,
                mimetype=file_data.mimetype,
                as_attachment=True,
                download_name=file_data.name
            )
        else:
            logging.error(f"File with UUID {uuid} not found.")
            abort(404, description=f"File with UUID {uuid} not found.")

# Initialize Flask app
app = Flask(__name__)

# Predefined metadata for testing
initial_metadata = {
    "1234": FileMetadata(
        uuid="1234",
        create_datetime="2023-09-20T12:34:56Z",
        size=12345,
        mimetype="text/plain",
        name="example.txt",
        path=os.path.join(BASE_DIR, "example.txt")
    )
}

file_service = FileService(files_metadata=initial_metadata)
file_api = FileAPI(app, file_service)

if __name__ == "__main__":
    app.run(debug=True)
