import random
import time
import pandas as pd

from app.extensions import socket_io
from wsgi import celery

from app.namespaces.utils.interface import SellerFirmNotificationInterface


@celery.task(bind=True, name='api.app.tasks.asyncr.async_handle_account_data_upload')
def async_handle_account_data_upload(self, file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: SellerFirmNotificationInterface):
    from app.namespaces.account.service import AccountService
    response_object = AccountService.handle_account_data_upload(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data)

    return response_object

@celery.task(bind=True, name='api.app.tasks.asyncr.async_handle_distance_sale_data_upload')
def async_handle_distance_sale_data_upload(self, file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: SellerFirmNotificationInterface):
    from app.namespaces.distance_sale.service import DistanceSaleService
    response_object = DistanceSaleService.handle_distance_sale_data_upload(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data)

    return response_object


@celery.task(bind=True, name='api.app.tasks.asyncr.async_handle_item_data_upload')
def async_handle_item_data_upload(self, file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: SellerFirmNotificationInterface):
    from app.namespaces.item.service import ItemService
    response_object = ItemService.handle_item_data_upload(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data)

    return response_object


@celery.task(bind=True, name='api.app.tasks.asyncr.async_handle_vatin_data_upload')
def async_handle_vatin_data_upload(self, file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: SellerFirmNotificationInterface):
    from app.namespaces.tax.vatin.service import VATINService
    response_object = VATINService.handle_vatin_data_upload(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data)

    return response_object


@celery.task(bind=True, name='api.app.tasks.asyncr.async_handle_transaction_input_data_upload')
def async_handle_transaction_input_data_upload(self, file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, seller_firm_id: int, seller_firm_notification_data: SellerFirmNotificationInterface, platform_code: str, data_retrieval: bool = False):
    from app.namespaces.transaction_input.service import TransactionInputService
    response_object = TransactionInputService.handle_transaction_input_data_upload(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, seller_firm_id, seller_firm_notification_data, platform_code, data_retrieval)

    return response_object



# registration of seller firms
@celery.task(bind=True, name='api.app.tasks.asyncr.async_handle_seller_firm_data_upload')
def async_handle_seller_firm_data_upload(self, file_path_in: str, file_type: str, df_encoding: str, delimiter: str, basepath: str, user_id: int, claimed: bool, seller_firm_notification_data: SellerFirmNotificationInterface):
    from app.namespaces.business.seller_firm.service import SellerFirmService
    response_object = SellerFirmService.handle_seller_firm_data_upload(file_path_in, file_type, df_encoding, delimiter, basepath, user_id, claimed, seller_firm_notification_data)

    return response_object












# #### FOR TESTING PURPOSES, INCLUDES USAGE OF WEBSOCKET

# @celery.task(bind=True)
# def long_task(self, room):
#     """
#     Defines a background task that runs a long function with progress
#     reports (Retrieved from https://blog.miguelgrinberg.com/post/using-celery-with-flask).
#     """

#     message = 'here comes the message'
#     total = random.randint(5, 10)
#     for i in range(total):
#         time.sleep(2)
#         meta = {"current": i, "total": total, "status": message,
#                 'result': 'pending...', "room": room}
#         self.update_state(state='PROGRESS', meta=meta)

#         socket_io.emit(
#             'message',
#             meta,
#             room=room,
#             namespace='/status'
#         )

#     result = {
#         "current": 100,
#         "total": 100,
#         "status": "Task completed!",
#         "result": '42',
#         "room": room
#     }
#     socket_io.emit('message', result, room=room, namespace='/status')

#     return result
