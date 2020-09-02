import random
from datetime import datetime, timedelta
from celery.task.base import periodic_task
from werkzeug.exceptions import HTTPException

#from wsgi import celery
from wsgi import app

#The periodic task schedules uses the UTC time zone by default, but you can change the time zone used using the timezone setting.
#https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html



# Clean up
@periodic_task(run_every=timedelta(hours=1))
def periodic_vatin_validation():
    with app.app_context():
        from app.namespaces.tax.vatin.service import VATINService
        from ..asyncr import async_process_validation_request
        vatin_list = VATINService.get_unvalidated(limit=50)
        app.logger.info('Unvalidated vatins: {}'.format(len(vatin_list)))
        if len(vatin_list) > 0:
            for i, vatin in enumerate(vatin_list):
                vatin_data = {
                    'country_code': vatin.country_code,
                    'number': vatin.number
                }

                # Auto retry takes list of expected exceptions and retry task when one of these occurs.
                # In that case always set max_retries boundary.
                # Never let tasks repeat infinitely.
                async_process_validation_request.apply_async(
                    eta=datetime.now() + timedelta(seconds=i * random.randint(25, 45)),
                    auto_retry=[HTTPException],
                    max_retries=1,
                    args=[vatin_data])
