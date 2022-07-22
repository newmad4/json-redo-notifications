import json
import logging
from abc import ABC, abstractmethod

from exceptions import EmptyMandatoryParameterError, ProviderError

logger = logging.getLogger(__name__)


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class NotificationBaseCheckMixin:
    """Mixin with basic validations."""

    mandatory_parameters = ("name",)

    def validate_data(self, notification_type: str, data: dict) -> None:
        errors = list()
        for parameter_name in self.mandatory_parameters:
            if not data.get(parameter_name):
                errors.append(parameter_name)

        if not errors:
            return None

        parameters_name = ", ".join(errors)
        raise EmptyMandatoryParameterError(
            f'Invalid data for notification type: "{notification_type}" '
            f'parameters: "{parameters_name}" {"is" if len(errors) == 1 else "are"} required. '
            f'Data: {data}.'
        )


class AbstractNotificationService(ABC):
    """Abstract class for notification services."""

    mandatory_parameters: tuple
    destination_parameter_name: str

    @abstractmethod
    def send(self, destination_parameter_value: str, data: dict):
        raise NotImplemented


@singleton
class EmailService(AbstractNotificationService, NotificationBaseCheckMixin):
    """Service for send email."""

    mandatory_parameters = ("name", "email")
    destination_parameter_name = "email"

    def send(self, email: str, data: dict) -> None:
        print(f"EMAIL sent to {email}. Data: {data}")


@singleton
class SMSService(AbstractNotificationService, NotificationBaseCheckMixin):
    """Service for send SMS."""

    mandatory_parameters = ("name", "phone")
    destination_parameter_name = "phone"

    def send(self, phone: str, data: dict) -> None:
        print(f"SMS sent to {phone}. Data: {data}")


@singleton
class PostService(AbstractNotificationService, NotificationBaseCheckMixin):
    """Service for make request to external API endpoints."""

    mandatory_parameters = ("name", "url")
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
            logger.warning("Unprocessed notification type!")
            return None
        return service()


class NotificationService:
    """Main service for send different notification types."""

    def __init__(self):
        self.processed_notifications = list()

    def send(self, data) -> None:
        notification_type = data["type"]
        service = factory.get_service(notification_type)
        try:
            service.validate_data(notification_type, data)
        except EmptyMandatoryParameterError as err:
            logger.warning(err)
            return None

        try:
            service.send(data[service.destination_parameter_name], data)
        except ProviderError as err:
            logger.error(err)
            return None
        self.processed_notifications.append(data)

    def log_success_results(self):
        with open("processed_notifications.json", "w") as f:
            json.dump(self.processed_notifications, f, indent=2)


factory = NotificationFactory()
factory.register_type("post", PostService)
factory.register_type("email", EmailService)
factory.register_type("sms", SMSService)
