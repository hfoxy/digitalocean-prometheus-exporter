import json

import requests


class API:

    __DIGITALOCEAN_API_URL = "https://api.digitalocean.com"

    def __init__(self, do, timeout: int):
        self.do = do
        self.timeout = timeout

    def get(self, path, params: dict = None):
        if params is None:
            params = dict()

        headers = {"Authorization": f"Bearer {self.do.token}"}
        response = requests.get(f"{self.__DIGITALOCEAN_API_URL}{path}", params, headers=headers, timeout=self.timeout)
        return json.loads(response.content)
