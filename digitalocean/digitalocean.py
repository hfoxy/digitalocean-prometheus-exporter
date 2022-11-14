from digitalocean.api import API
from digitalocean.droplets import Droplets


class DigitalOcean:

    def __init__(self, token: str, timeout: int = 10):
        self.token = token
        self.api = API(self, timeout=timeout)

    def get_all_droplets(self):
        return Droplets(self.api.get("/v2/droplets")['droplets']).droplet_list
