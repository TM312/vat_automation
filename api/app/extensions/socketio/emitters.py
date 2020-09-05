from flask import (
    current_app,
    session)

from flask_socketio import (emit, join_room, leave_room, rooms)
from app.extensions import socket_io


class SocketService:

    @staticmethod
    def emit_status(meta):
        socket_io.emit(
            'status',
            meta
        )

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
