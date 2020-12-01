from datetime import datetime, timedelta, date
# from celery.task.base import periodic_task
from celery.schedules import crontab

#from wsgi import celery
from wsgi import app

#The periodic task schedules uses the UTC time zone by default, but you can change the time zone used using the timezone setting.
#https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html



# # Up to date
# @periodic_task(run_every=timedelta(minutes=20)) #crontab(hour=20, minute=14))  # timedelta(minutes=1)
# def daily_exchange_rates_ecb():
#     # https://stackoverflow.com/questions/46540664/no-application-found-either-work-inside-a-view-function-or-push-an-application
#     with app.app_context():
#         from app.namespaces.exchange_rate import ExchangeRate
#         from app.namespaces.exchange_rate.service import ExchangeRateService
#         app.logger.info('running daily_exchange_rates_ecb')

#         # Test with two example rates
#         exchange_rates_EUR_today = ExchangeRateService.get_list_by_base_date('EUR', date.today())

#         if isinstance(exchange_rates_EUR_today, list) and len(exchange_rates_EUR_today) > 0:

#             app.logger.info('Exchange Rates ALREADY existing')

#         else:
#             app.logger.info('Exchange Rates NOT existing')

#             supported_currencies = app.config.SUPPORTED_CURRENCIES
#             app.logger.info('supported_currencies:{}'.format(supported_currencies))

#             exchange_rate_dict = ExchangeRateService.retrieve_ecb_exchange_rates()
#             #exchange_rate_dict = {'USD': '1.1870', 'JPY': '122.66', 'BGN': '1.9558', 'CZK': '26.667', 'DKK': '7.4493', 'GBP': '0.90430', 'HUF': '359.02', 'PLN': '4.5263', 'RON': '4.8670', 'SEK': '10.2805', 'CHF': '1.0682', 'ISK': '163.50', 'NOK': '10.9203', 'HRK': '7.5590', 'RUB': '92.4200', 'TRY': '10.1489', 'AUD': '1.6359', 'BRL': '6.6072', 'CAD': '1.5525', 'CNY': '7.8468', 'HKD': '9.2030', 'IDR': '16943.12', 'ILS': '4.0076', 'INR': '88.0085', 'KRW': '1332.60', 'MXN': '24.6840', 'MYR': '4.9005', 'NZD': '1.7507', 'PHP': '57.192', 'SGD': '1.5999', 'THB': '36.287', 'ZAR': '18.6933'}

#             try:
#                 ExchangeRateService.process_ecb_rates(date.today(), exchange_rate_dict, supported_currencies)
#                 app.logger.info('Worked')
#             except Exception as e:
#                 app.logger.info('Didnt Work')
#                 app.logger.info(e)


#             # app.logger.info('exchange_rate_dict')
#             # app.logger.info(exchange_rate_dict)
