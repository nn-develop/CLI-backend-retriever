import requests

class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_file_stat(self, uuid):
        url = f"{self.base_url}/file/{uuid}/stat/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise FileNotFoundError(f"File with UUID {uuid} not found.")
        else:
            response.raise_for_status()

    def read_file(self, uuid):
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
