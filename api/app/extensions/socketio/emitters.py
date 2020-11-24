from typing import List

from flask import (
    current_app,
    session)

from flask_socketio import (emit, join_room, leave_room, rooms)
from app.extensions import socket_io


class SocketService:

    # @staticmethod
    # def emit_clear_objects(object_type: str):
    #     socket_io.emit(
    #         'clear_{}s'.format(object_type)
    #     )

    # @staticmethod
    # def emit_new_object(meta, object_type):
    #     socket_io.emit(
    #         'new_{}'.format(object_type),
    #         meta
    #     )

    # @staticmethod
    # def emit_update_object(meta, object_type):
    #     socket_io.emit(
    #         'update_{}'.format(object_type),
    #         meta
    #     )

    # @staticmethod
    # def emit_new_objects(meta, object_type):
    #     socket_io.emit(
    #         'new_{}s'.format(object_type),
    #         meta
    #     )


    # @staticmethod
    # def emit_status(meta):
    #     socket_io.emit(
    #         'status',
    #         meta
    #     )

    # @staticmethod
    # def emit_status_success(current: int, total: int, target: str, object_type: str):

    #     if current == 1 or current % 25 == 0 or current == total:

    #         status = {
    #             'current': current,
    #             'total': total,
    #             'target': target,
    #             'done': False,
    #             'object': object_type,
    #         }

    #         SocketService.emit_status(meta=status)


    # @staticmethod
    # def emit_status_info(object_type: str, message: str):

    #     status = {
    #         'target': 'infobox',
    #         'total': 0,
    #         'done': True,
    #         'object': object_type,
    #         'message': message
    #     }

    #     SocketService.emit_status(meta=status)

    # @staticmethod
    # def emit_status_warning(object_type: str, message: str):

    #     status = {
    #         'target': 'warningbox',
    #         'total': 0,
    #         'done': True,
    #         'object': object_type,
    #         'message': message
    #     }

    #     SocketService.emit_status(meta=status)

    # @staticmethod
    # def emit_status_error(object_type: str, message: str):

    #     status = {
    #         'target': 'errorbox',
    #         'done': False,
    #         'object': object_type,
    #         'message': message
    #     }

    #     SocketService.emit_status(meta=status)

    # @staticmethod
    # def emit_status_error_invalid_file(message: str):
    #     status = {
    #         'target': 'errorbox',
    #         'done': True,
    #         'object': 'file',
    #         'message': message,
    #     }
    #     SocketService.emit_status(meta=status)

    # @staticmethod
    # def emit_status_error_no_value(current: int, object_type: str, column_name: str):
    #     message = 'No value in column "{}", row {}.'.format(column_name, current+1)
    #     SocketService.emit_status_error(object_type, message)

    # @staticmethod
    # def emit_status_error_invalid_value(object_type: str, message: str):
    #     SocketService.emit_status_error(object_type, message)


    # @staticmethod
    # def emit_status_error_column_read(current: int, object_type: str, column_name: str):
    #     message = 'Can not read column "{}" in row {}.'.format(column_name, current+1)
    #     SocketService.emit_status_error(object_type, message)


    # @staticmethod
    # def emit_status_error_no_seller_firm(object_type: str):
    #     message = 'Can not identify the seller firm for the uploaded data.'
    #     SocketService.emit_status_error(object_type, message)

    # @staticmethod
    # def emit_status_error_unidentifiable_object(object_type: str, object_str: str, current: int):
    #     message = 'Can not identify the {} in row {}. Have you uploaded all necessary data?'.format(object_str, current+1)
    #     SocketService.emit_status_error(object_type, message)



    # @staticmethod
    # def emit_status_final(total: int, target: str, object_type: str, object_type_human_read: str, duplicate_list: List):

    #     if total == 0:
    #         message = 'The upload was successful but all {}s had been processed before already.'.format(object_type_human_read)
    #     elif total == 1:
    #         message = '{} new {} has been successfully registered.'.format(total, object_type_human_read)
    #     else:
    #         message = '{} new {}s have been successfully registered.'.format(total, object_type_human_read)

    #     status = {
    #         'total': total,
    #         'target': target,
    #         'done': True,
    #         'object': object_type,
    #         'message': message
    #     }
    #     SocketService.emit_status(meta=status)

    #     if len(duplicate_list) > 0:
    #         if len(duplicate_list) == 1:
    #             message = 'The uploaded {} "{}" had already been registered.'.format(object_type_human_read, duplicate_list[0])
    #         elif len(duplicate_list) == 2:
    #             message = 'The uploaded {}s "{}" and "{}" had already been registered.'.format(object_type_human_read, duplicate_list[0], duplicate_list[1])
    #         else:
    #             message = 'The {} "{}" and {} others had been uploaded before.'.format(object_type_human_read, duplicate_list[0], len(duplicate_list)-1)

    #         status = {
    #             'target': 'infobox',
    #             'total': 0,
    #             'done': True,
    #             'object': object_type,
    #             'message': message,
    #             'duplicate_list': duplicate_list
    #         }

    #         SocketService.emit_status(meta=status)


    #use during seed
    @staticmethod
    def emit_clear_objects(*args, **kwargs):
        pass
    @staticmethod
    def emit_new_object(*args, **kwargs):
        pass
    @staticmethod
    def emit_update_object(*args, **kwargs):
        pass
    @staticmethod
    def emit_new_objects(*args, **kwargs):
        pass
    @staticmethod
    def emit_status(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_success(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_info(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_warning(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_error(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_error_invalid_file(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_error_no_value(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_error_invalid_value(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_error_column_read(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_error_no_seller_firm(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_error_unidentifiable_object(*args, **kwargs):
        pass
    @staticmethod
    def emit_status_final(*args, **kwargs):
        pass
