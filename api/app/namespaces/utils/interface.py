from mypy_extensions import TypedDict
from typing import Union
from datetime import datetime


class NotificationInterface(TypedDict, total=False):
    id: int
    created_on: datetime
    subject: str
    status: str
    message: str
    n_type: str


class TransactionNotificationInterface(NotificationInterface):
    transaction_id: int
    original_filename: str
    reference_value: Union[str, int, float]
    calculated_value: Union[str, int, float]


class SellerFirmNotificationInterface(NotificationInterface):
    seller_firm_id: int
    created_by: int
