from flask import (
    current_app,
    session)

from flask_socketio import (emit, join_room, leave_room, rooms)
from app.extensions import socket_io


class SocketService:

    @staticmethod
    def emit_new_account(meta):
        socket_io.emit(
            'new_account',
            meta
        )

    @staticmethod
    def emit_new_item(meta):
        socket_io.emit(
            'new_item',
            meta
        )

    @staticmethod
    def emit_new_vat_number(meta):
        socket_io.emit(
            'new_vat_number',
            meta
        )

    @staticmethod
    def emit_new_distance_sale(meta):
        socket_io.emit(
            'new_distance_sale',
            meta
        )

    @staticmethod
    def emit_status(meta):
        socket_io.emit(
            'status',
            meta
        )

    @staticmethod
    def emit_status_error(current, total, original_filename, object_type, title):

        status = {
            'current': current,
            'total': total,
            'original_filename': original_filename,
            'variant': 'danger',
            'done': False,
            'object': object_type,
            'title': title
        }

        SocketService.emit_status(meta=status)

    @staticmethod
    def emit_status_error_no_value(current, total, original_filename, object_type, column_name):
        title = 'No value in column "{}", row {}.'.format(column_name, current)
        SocketService.emit_status_error(current, total, original_filename, object_type, title)

    @staticmethod
    def emit_status_success(current, total, original_filename, object_type, title):

        status = {
            'current': current,
            'total': total,
            'original_filename': original_filename,
            'variant': '',
            'done': False,
            'object': object_type,
            'title': title
        }

        SocketService.emit_status(meta=status)

    @staticmethod
    def emit_status_final(current, total, original_filename, object_type, title):
        status = {
            'current': current,
            'total': total,
            'original_filename': original_filename,
            'variant': 'success',
            'done': True,
            'object': object_type,
            'title': title
        }

        SocketService.emit_status(meta=status)
