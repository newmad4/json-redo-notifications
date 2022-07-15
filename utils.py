import requests

from settings import REDO_DATA_SOURCE_URL


def fetch_notifications_data() -> list:
    response = requests.get(REDO_DATA_SOURCE_URL)
    return response.json()
