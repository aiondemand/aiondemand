import requests


def get_hello_world():
    url = "https://api.aiod.eu/counts/v1"
    counts = requests.get(url)
    return counts
