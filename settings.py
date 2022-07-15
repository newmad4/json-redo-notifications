import os

from dotenv import load_dotenv

load_dotenv()

REDO_DATA_SOURCE_URL = os.getenv(
    "REDO_DATA_SOURCE_URL",
    default="https://raw.githubusercontent.com/UN-ICC/notifications-processor/master/notifications_log.json"
)
