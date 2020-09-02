import random
from datetime import datetime, timedelta
from celery.task.base import periodic_task

#from wsgi import celery
from wsgi import app

#The periodic task schedules uses the UTC time zone by default, but you can change the time zone used using the timezone setting.
#https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html



# # Up to date
# @periodic_task(run_every=timedelta(minutes=1))
# def daily_exchange_rates_ecb():
#     # https://stackoverflow.com/questions/46540664/no-application-found-either-work-inside-a-view-function-or-push-an-application
#     with app.app_context():
#         from app.namespaces.exchange_rate.service import ExchangeRateService

#         exchange_rate_dict = ExchangeRateService.retrieve_ecb_exchange_rates()

#         print('', flush=True)
#         print('exchange_rate_dict', flush=True)
#         print(exchange_rate_dict, flush=True)
#         print('', flush=True)
