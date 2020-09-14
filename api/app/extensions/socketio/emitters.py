from typing import List

from flask import (
    current_app,
    session)

from flask_socketio import (emit, join_room, leave_room, rooms)
from app.extensions import socket_io


class SocketService:

    @staticmethod
    def emit_new_object(meta, object_type):
        socket_io.emit(
            'new_{}'.format(object_type),
            meta
        )

    @staticmethod
    def emit_new_objects(meta, object_type):
        socket_io.emit(
            'new_{}s'.format(object_type),
            meta
        )


    @staticmethod
    def emit_status(meta):
        socket_io.emit(
            'status',
            meta
        )

    @staticmethod
    def emit_status_success(current: int, total: int, target: str, object_type: str):

        if current == 1 or current % 25 == 0 or current == total:

            status = {
                'current': current,
                'total': total,
                'target': target,
                'done': False,
                'object': object_type,
            }

            SocketService.emit_status(meta=status)


    @staticmethod
    def emit_status_info(object_type: str, message: str):

        status = {
            'target': 'infobox',
            'total': 0,
            'done': True,
            'object': object_type,
            'message': message
        }

        SocketService.emit_status(meta=status)

    @staticmethod
    def emit_status_warning(object_type: str, message: str):

        status = {
            'target': 'warningbox',
            'total': 0,
            'done': True,
            'object': object_type,
            'message': message
        }

        SocketService.emit_status(meta=status)

    @staticmethod
    def emit_status_error(current: int, total: int, object_type: str, message: str):

        status = {
            'target': 'errorbox',
            'done': False,
            'object': object_type,
            'message': message
        }

        SocketService.emit_status(meta=status)

    @staticmethod
    def emit_status_error_no_value(current: int, object_type: str, column_name: str):
        message = 'No value in column "{}", row {}.'.format(column_name, current)
        SocketService.emit_status_error(object_type, message)

    @staticmethod
    def emit_status_error_column_read(current: int, object_type: str, column_name: str):
        message = 'Can not read column "{}" in row {}.'.format(column_name, current)
        SocketService.emit_status_error(object_type, message)


    @staticmethod
    def emit_status_error_no_seller_firm(object_type: str):
        message = 'Can not identify the seller firm for the uploaded data. Please retry later or contact one of the admins.'
        SocketService.emit_status_error(object_type, message)



    @staticmethod
    def emit_status_final(total: int, target: str, object_type: str, object_type_human_read: str, duplicate_list: List):

        if total == 0:
            message = 'The upload was successful but all {}s had been processed before already.'.format(object_type_human_read)
        elif total == 1:
            message = '{} new {} has been successfully registered.'.format(total, object_type_human_read)
        else:
            message = '{} new {}s have been successfully registered.'.format(total, object_type_human_read)

        status = {
            'total': total,
            'target': target,
            'done': True,
            'object': object_type,
            'message': message
        }
        SocketService.emit_status(meta=status)

        if len(duplicate_list) > 0:
            if len(duplicate_list) == 1:
                message = 'The uploaded {} "{}" had already been registered.'.format(object_type_human_read, duplicate_list[0])
            elif len(duplicate_list) == 2:
                message = 'The uploaded {}s "{}" and "{}" had already been registered.'.format(object_type_human_read, duplicate_list[0], duplicate_list[1])
            else:
                message = 'The {} "{}" and {} other ones had been uploaded before.'.format(object_type_human_read, duplicate_list[0], len(duplicate_list)-1)

            status = {
                'target': 'infobox',
                'total': 0,
                'done': True,
                'object': object_type,
                'message': message,
                'duplicate_list': duplicate_list
            }

            SocketService.emit_status(meta=status)
