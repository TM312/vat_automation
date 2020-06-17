from mypy_extensions import TypedDict
from datetime import datetime


class NotificationInterface(TypedDict, total=False):
    id: int
    created_on: datetime
    subject: str
    status: str
    message: str
    n_type: str


class TransactionNotificationInterface(NotificationInterface):
    transaction_input_id: int
    original_filename: str
