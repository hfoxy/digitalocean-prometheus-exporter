from digitalocean.api import API
from digitalocean.droplets import Droplets


class DigitalOcean:

    def __init__(self, tokens: list[str], timeout: int = 10):
        self.tokens = tokens
        self.api = API(self, timeout=timeout)

    def get_all_droplets(self):
        return Droplets(self.api.get("/v2/droplets", {'page': 1, 'per_page': 1000})['droplets']).droplet_list
