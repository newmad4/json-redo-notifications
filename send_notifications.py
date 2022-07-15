import json

import requests

REDO_DATA_SOURCE_URL = "https://raw.githubusercontent.com/UN-ICC/notifications-processor/master/notifications_log.json"
MANDATORY_FIELDS = {
    "sms": ("phone", "name"),
    "email": ("email", "name"),
    "post": ("url", "name"),
}


def fetch_notifications_data() -> list:
    response = requests.get(REDO_DATA_SOURCE_URL)
    return response.json()


def send_sms(phone: str, data: dict) -> None:
    print(f"SMS sent to {phone}. Data: {data}")


def send_email(email: str, data: dict) -> None:
    print(f"EMAIL sent to {email}. Data: {data}")


def send_post(url: str, data: dict) -> None:
    print(f"POST sent to {url}. Data: {data}")


def is_valid_data(notification_type: str, data: dict) -> bool:
    for parameter_name in MANDATORY_FIELDS.get(notification_type):
        if not data.get(parameter_name):
            return False
    return True


processed_data = list()
for data in fetch_notifications_data():
    notification_type = data["type"]

    if not is_valid_data(notification_type, data):
        print(f"Invalid notification data: {data}")
        continue

    notification_was_sent = True
    if notification_type == "sms":
        send_sms(data["phone"], data)
    elif notification_type == "email":
        send_email(data["email"], data)
    elif notification_type == "post":
        send_email(data["url"], data)
    else:
        notification_was_sent = False
        print("Unprocessed notification type!")

    if notification_was_sent:
        processed_data.append(data)

with open("processed_notifications.json", "w") as f:
    json.dump(processed_data, f, indent=2)
