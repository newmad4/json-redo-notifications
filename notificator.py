from concurrent.futures import ThreadPoolExecutor

from services import NotificationService
from utils import fetch_notifications_data


def send_notifications() -> None:
    notificator = NotificationService()

    with ThreadPoolExecutor() as executor:
        for data in fetch_notifications_data():
            executor.submit(
                notificator.send,
                data
            )

    notificator.log_success_results()

