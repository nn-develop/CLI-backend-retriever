import requests

class RestClient:
    """
    Client for interacting with a REST API to manage files.
    """
    def __init__(self, base_url):
        """
        Initialize RestClient with base URL.
        
        :param base_url: Base URL for the REST API.
        """
        self.base_url = base_url

    def get_file_stat(self, uuid):
        """
        Get file metadata by UUID.
        
        :param uuid: UUID of the file.
        """
        url = f"{self.base_url}/file/{uuid}/stat/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise FileNotFoundError(f"File with UUID {uuid} not found.")
        else:
            response.raise_for_status()

    def read_file(self, uuid):
        """
        Read file content by UUID.
        
        :param uuid: UUID of the file.
        """
        url = f"{self.base_url}/file/{uuid}/read/"
        response = requests.get(url)
        if response.status_code == 200:
            file_name = response.headers.get('Content-Disposition', 'file')
            file_content = response.content
            return file_name, file_content
        elif response.status_code == 404:
            raise FileNotFoundError(f"File with UUID {uuid} not found.")
        else:
            response.raise_for_status()
