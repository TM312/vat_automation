import random
import time

from app.extensions import socket_io
from wsgi import celery


@celery.task(bind=True)
def long_task(self, room):
    """
    Defines a background task that runs a long function with progress
    reports (Retrieved from https://blog.miguelgrinberg.com/post/using-celery-with-flask).
    """

    message = 'here comes the message'
    total = random.randint(5, 10)
    for i in range(total):
        time.sleep(2)
        meta = {"current": i, "total": total, "status": message,
                'result': 'pending...', "room": room}
        self.update_state(state='PROGRESS', meta=meta)

        socket_io.emit(
            'message',
            meta,
            room=room,
            namespace='/status'
        )

    result = {
        "current": 100,
        "total": 100,
        "status": "Task completed!",
        "result": '42',
        "room": room
    }
    socket_io.emit('message', result, room=room, namespace='/status')

    return result
