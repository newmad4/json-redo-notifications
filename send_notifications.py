import requests

REDO_DATA_SOURCE_URL = "https://raw.githubusercontent.com/UN-ICC/notifications-processor/master/notifications_log.json"


def fetch_notifications_data() -> list:
    response = requests.get(REDO_DATA_SOURCE_URL)
    return response.json()

print(fetch_notifications_data())
