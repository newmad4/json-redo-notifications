from services import NotificationService
from utils import fetch_notifications_data

notificator = NotificationService()

for data in fetch_notifications_data():
    notificator.send(data)

notificator.log_success_results()
