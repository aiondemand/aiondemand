import requests
from urllib.parse import urljoin

API_BASE_URL = "https://api.aiod.eu/"


def get(endpoint: str) -> dict:
    url = urljoin(API_BASE_URL, endpoint)
    res = requests.get(url)
    res.raise_for_status()

    return res.json()


def post(endpoint: str):
    pass


def put(endpoint: str):
    pass


def delete(endpoint: str):
    pass
