import json

import requests

from services import NotificationService

REDO_DATA_SOURCE_URL = "https://raw.githubusercontent.com/UN-ICC/notifications-processor/master/notifications_log.json"
MANDATORY_FIELDS = {
    "sms": ("phone", "name"),
    "email": ("email", "name"),
    "post": ("url", "name"),
}


def fetch_notifications_data() -> list:
    response = requests.get(REDO_DATA_SOURCE_URL)
    return response.json()


notificator = NotificationService()
for data in fetch_notifications_data():
    try:
        notificator.send(data)
    except ValueError as err:
        print(err)
        continue

notificator.log_success_results()
