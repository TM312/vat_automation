
from os import path
import pandas as pd
import more_itertools as mit

from datetime import date, datetime, timedelta
from app.extensions import db
from app.namespaces.exchange_rate.service import ExchangeRateService
from app.namespaces.exchange_rate import ExchangeRate
from werkzeug.exceptions import UnsupportedMediaType, InternalServerError





class ExchangeRatesSeedService:

    @staticmethod
    def get_date_or_None_incl_format(df: pd.DataFrame, i: int, column: str, dstr_format: str, alternative_dstr_format: str) -> date:
        if pd.isnull(df.iloc[i][column]):
            return None
        else:
            try:
                date = datetime.strptime(df.iloc[i][column], dstr_format).date()
            except:
                try:
                    date = datetime.strptime(
                        df.iloc[i][column], alternative_dstr_format).date()
                except:
                    raise UnsupportedMediaType('Can not read date format.')
        return date

    @staticmethod
    def create_historic_exchange_rates():
        file = 'hist_exchange_rates.csv'
        SUPPORTED_CURRENCIES = ['GBP', 'CZK', 'PLN']#, 'HUF', 'DKK', 'SEK', 'CHF', 'NOK']
        SERVICE_START_DATE = datetime.strptime('01-05-2019', '%d-%m-%Y').date()
        timespan_as_days = (date.today()-SERVICE_START_DATE).days


        from . import BASE_PATH_SEEDS

        dirpath = path.join(BASE_PATH_SEEDS, file)
        df = pd.read_csv(dirpath)
        counter = 0


        for i in range(timespan_as_days+1):
            exchange_rate_date = SERVICE_START_DATE + timedelta(days=i)
            calc_exchange_rate_date = exchange_rate_date
            date_string = exchange_rate_date.strftime('%Y-%m-%d')

            #below you find the worst code ever
            while date_string not in df['Date'].values:
                calc_exchange_rate_date -=  timedelta(days=1)
                date_string = calc_exchange_rate_date.strftime('%Y-%m-%d')
                print('date: {} not in csv'.format(date_string), flush=True)


            row = df.loc[df['Date'] == date_string]


            for currency_code in SUPPORTED_CURRENCIES:
                value = row[currency_code].values[0]

                exchange_rate_data = {
                    'source': 'ECB',
                    'date': exchange_rate_date,
                    'base': 'EUR',
                    'target': currency_code,
                    'rate': round(value, 5)
                }
                print('exchange_rate_data: source: {} | date: {} | calc_date {} | base: {} | target: {} | rate: {}'.format(
                    exchange_rate_data['source'],
                    exchange_rate_data['date'],
                    calc_exchange_rate_date,
                    exchange_rate_data['base'],
                    exchange_rate_data['target'],
                    exchange_rate_data['rate']
                    ), flush=True)
                print("", flush=True)

                ExchangeRateService.create(exchange_rate_data)
                counter += 1

                # creating reverse rates
                exchange_rate_data['base'] = currency_code
                exchange_rate_data['target'] = 'EUR'
                exchange_rate_data['rate'] = round(1/value, 5)

                ExchangeRateService.create(exchange_rate_data)
                counter += 1

                #creating same rates, i.e. 'EUR' to 'EUR'
                exchange_rate_data = {
                    'source': 'ECB',
                    'date': exchange_rate_date,
                    'base': currency_code,
                    'target': currency_code,
                    'rate': 1
                }

                ExchangeRateService.create(exchange_rate_data)
                counter += 1

            currency_tuples = list(mit.distinct_combinations(SUPPORTED_CURRENCIES, 2))

            for currency_tuple in currency_tuples:
                ExchangeRateService.create_between_rate(exchange_rate_date, base=currency_tuple[0], target=currency_tuple[1])
                counter += 1

            exchange_rate_date += timedelta(days=1)

        response_object = {
            'status': 'success',
            'message': 'Successfully created historic exchange rates ({} objects)'.format(str(counter))
        }
        return response_object
