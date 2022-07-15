import json
from abc import ABC, abstractmethod

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


class AbstractNotificationService(ABC):
    """Abstract class for notification services."""

    destination_parameter_name: str

    @abstractmethod
    def send(self, destination_parameter_value: str, data: dict):
        raise NotImplemented


class EmailService(AbstractNotificationService):
    """Service for send email."""

    destination_parameter_name = "email"

    def send(self, email: str, data: dict) -> None:
        print(f"EMAIL sent to {email}. Data: {data}")


class SMSService(AbstractNotificationService):
    """Service for send SMS."""

    destination_parameter_name = "phone"

    def send(self, phone: str, data: dict) -> None:
        print(f"SMS sent to {phone}. Data: {data}")


class PostService(AbstractNotificationService):
    """Service for make request to external API endpoints."""

    destination_parameter_name = "url"

    def send(self, url: str, data: dict) -> None:
        print(f"POST sent to {url}. Data: {data}")


class NotificationFactory:
    """Factory class for registration and get service by notification type."""

    def __init__(self):
        self._services = {}

    def register_type(self, notification_type, service) -> None:
        self._services[notification_type] = service

    def get_service(self, notification_type):
        service = self._services.get(notification_type)
        if not service:
            print("Unprocessed notification type!")
            return None
        return service()


factory = NotificationFactory()
factory.register_type("post", PostService)
factory.register_type("email", EmailService)
factory.register_type("sms", SMSService)
