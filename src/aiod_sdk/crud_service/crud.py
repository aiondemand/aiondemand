import requests
from urllib.parse import urljoin

API_BASE_URL = "https://api.aiod.eu/"


def get(endpoint: str) -> requests.Response:
    url = urljoin(API_BASE_URL, endpoint)
    res = requests.get(url)

    return res


def post(endpoint: str):
    pass


def put(endpoint: str):
    pass


def delete(endpoint: str):
    pass
