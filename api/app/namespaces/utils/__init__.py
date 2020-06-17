from .model import Notification, TransactionNotification
from .schema import notification_dto, transaction_notification_dto

BASE_ROUTE = "utils"


def attach_utils(api, app):
    from .controller import ns as utils_ns
    api.add_namespace(utils_ns, path=f"/{BASE_ROUTE}")
