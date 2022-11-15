import json
import math
import time
import requests


class API:

    __DIGITALOCEAN_API_URL = "https://api.digitalocean.com"

    def __init__(self, manager, timeout: int):
        self.manager = manager
        self.timeout = timeout
        self.tokens = manager.tokens
        self.token_limits = {}

        for token in self.tokens:
            self.token_limits[token] = RateLimits()

    def get_token(self):
        options: list[TokenOption] = list[TokenOption]()

        epoch = math.floor(time.time())
        for token in self.tokens:
            token_limit = self.token_limits[token]

            if token_limit.remaining > 0 or token_limit.reset <= epoch:
                diff = token_limit.reset - epoch
                req_per_minute = token_limit.remaining / (diff / 60)
                result = TokenOption(token, req_per_minute)
                options.append(result)

                if token_limit.reset == 0:
                    return token

        selected = None
        for option in options:
            if selected is None or selected.req_per_minute < option.req_per_minute:
                selected = option

        if selected is None:
            raise Exception('no available tokens')

        return selected.token

    def get(self, path, params: dict = None):
        if params is None:
            params = dict()

        token = self.get_token()
        token_limit = self.token_limits[token]
        print(f"using token {hex(hash(token))[2:]} ({token_limit.remaining}/{token_limit.limit})")

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{self.__DIGITALOCEAN_API_URL}{path}", params, headers=headers, timeout=self.timeout)
        if response.headers.get('RateLimit-Limit') is not None:
            token_limit.limit = int(response.headers.get('RateLimit-Limit'))

        if response.headers.get('RateLimit-Remaining') is not None:
            token_limit.remaining = int(response.headers.get('RateLimit-Remaining'))

        if response.headers.get('RateLimit-Reset') is not None:
            token_limit.reset = int(response.headers.get('RateLimit-Reset'))

        if response.status_code == 429:
            return self.get(path, params)

        return json.loads(response.content)


class RateLimits:

    def __init__(self):
        self.limit = 5000
        self.remaining = 5000
        self.reset = 0


class TokenOption:

    def __init__(self, token: str, req_per_minute: float):
        self.token = token
        self.req_per_minute = req_per_minute
