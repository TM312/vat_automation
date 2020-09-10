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
    def emit_status(meta):
        socket_io.emit(
            'status',
            meta
        )

    @staticmethod
    def emit_status_success(current: int, total: int, target: str, object_type: str, title: str):

        status = {
            'current': current,
            'total': total,
            'target': target,
            'variant': '',
            'done': False,
            'object': object_type,
            'title': title
        }

        SocketService.emit_status(meta=status)

    @staticmethod
    def emit_status_success_progress(current: int, total: int, target: str, object_type: str, object_type_human_read: str):
        title = 'New {}s are being registered...'.format(object_type_human_read)
        SocketService.emit_status_success(current, total, target, object_type, title)



    @staticmethod
    def emit_status_info_box(current: int, total: int, target: str, object_type: str, message: str):

        status = {
            'current': current,
            'total': total,
            'target': 'infobox',
            'variant': 'info',
            'done': False,
            'object': object_type,
            'message': message
        }

        SocketService.emit_status(meta=status)

    @staticmethod
    def emit_status_error(current: int, total: int, target: str, object_type: str, title: str):

        status = {
            'current': current,
            'total': total,
            'target': target,
            'variant': 'danger',
            'done': False,
            'object': object_type,
            'title': title
        }

        SocketService.emit_status(meta=status)

    @staticmethod
    def emit_status_error_no_value(current: int, total: int, target: str, object_type: str, column_name: str):
        title = 'No value in column "{}", row {}.'.format(column_name, current)
        SocketService.emit_status_error(current, total, target, object_type, title)

    @staticmethod
    def emit_status_error_column_read(current: int, total: int, target: str, object_type: str, column_name: str):
        title = 'Can not read column "{}" in row {}.'.format(column_name, current)
        SocketService.emit_status_error(current, total, target, object_type, title)


    @staticmethod
    def emit_status_error_no_seller_firm(current: int, total: int, target: str, object_type: str):
        title = 'Can not identify the seller firm for the uploaded data. Please retry later or contact one of the admins.'
        SocketService.emit_status_error(current, total, target, object_type, title)



    @staticmethod
    def emit_status_final(current: int, total: int, target: str, object_type: str, object_type_human_read: str):

        title = '{} {}s have been successfully registered.'.format(total, object_type_human_read)
        status = {
            'current': current,
            'total': total,
            'target': target,
            'variant': 'success',
            'done': True,
            'object': object_type,
            'title': title
        }

        SocketService.emit_status(meta=status)
