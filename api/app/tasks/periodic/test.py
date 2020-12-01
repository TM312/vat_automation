import random
from datetime import datetime, timedelta
# from celery.task.base import periodic_task

#from wsgi import celery
from wsgi import app

#The periodic task schedules uses the UTC time zone by default, but you can change the time zone used using the timezone setting.
#https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html



# @periodic_task(run_every=timedelta(seconds=10))
# def new_users():
#     with app.app_context():
#         from app.namespaces.user.tax_auditor.service import TaxAuditorService

#         i = random.randint(1,2000)

#         tax_auditor_data = {
#             'name': 'ta_' + str(i),
#             'email': 'ta_' + str(i) + '@mail.com',
#             'password': 'pw',
#             'role': 'employee'
#         }

#         TaxAuditorService.create(tax_auditor_data)
