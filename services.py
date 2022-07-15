from abc import ABC, abstractmethod


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
