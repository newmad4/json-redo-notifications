from services import NotificationService
from utils import fetch_notifications_data

notificator = NotificationService()
for data in fetch_notifications_data():
    try:
        notificator.send(data)
    except ValueError as err:
        print(err)
        continue

notificator.log_success_results()
