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

    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(5, 10)
    for i in range(total):
        time.sleep(10)
        if not message:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        meta = {"current": i, "total": total, "status": message, "room": room}
        self.update_state(state='PROGRESS', meta=meta)
        socket_io.emit(message, meta, room=room, namespace='/status')

    result = {
        "current": 100,
        "total": 100,
        "status": "Task completed!",
        "result": 42,
        "room": room
    }
    return result
