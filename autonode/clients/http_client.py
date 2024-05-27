import requests
from asgi_correlation_id import correlation_id


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, data, headers=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self.__add_correlation_id(headers)
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def post_file(self, endpoint, files, headers=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self.__add_correlation_id(headers)
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self.__add_correlation_id(headers)
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data, headers=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self.__add_correlation_id(headers)
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def __add_correlation_id(self, headers):
        if headers is None:
            headers = {"X-Request-ID": correlation_id.get() or ""}
        else:
            headers["X-Request-ID"] = correlation_id.get() or ""
        return headers
