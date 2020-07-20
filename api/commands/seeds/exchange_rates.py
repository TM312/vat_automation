
from os import path
import pandas as pd
import more_itertools as mit

from datetime import date, datetime
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
        SUPPORTED_CURRENCIES = ['GBP', 'CZK', 'PLN', 'HUF', 'DKK', 'SEK']
        SERVICE_START_DATE = datetime.strptime('01-06-2018', '%d-%m-%Y').date()

        from . import BASE_PATH_SEEDS


        dirpath = path.join(BASE_PATH_SEEDS, file)
        df = pd.read_csv(dirpath)
        counter = 0
        for row in range(len(df.index)):
            date = ExchangeRatesSeedService.get_date_or_None_incl_format(df, i=row, column='Date', dstr_format='%Y-%m-%d', alternative_dstr_format='%Y.%m.%d')
            if not date:
                response_object = {
                    'status': 'error',
                    'message': 'The corresponding exchange rate collection can not be found.'
                }
                raise InternalServerError(response_object)

            if date >= SERVICE_START_DATE:
                for currency_code in SUPPORTED_CURRENCIES:
                    value = round(df.iloc[row][currency_code], 5)
                    exchange_rate_data = {
                        'source': 'ECB',
                        'date': date,
                        'base': 'EUR',
                        'target': currency_code,
                        'rate': value
                    }
                    ExchangeRateService.create(exchange_rate_data)
                    counter +=1

                    # creating reverse rates
                    exchange_rate_data['base'] = currency_code
                    exchange_rate_data['target'] = 'EUR'
                    exchange_rate_data['rate'] = round(1/value, 5)

                    ExchangeRateService.create(exchange_rate_data)
                    counter += 1


                currency_tuples = list(mit.distinct_combinations(SUPPORTED_CURRENCIES, 2))
                for currency_tuple in currency_tuples:
                    ExchangeRateService.create_between_rate(date, base=currency_tuple[0], target=currency_tuple[1])
                    counter += 1
            else:
                break


        response_object = {
            'status': 'success',
            'message': 'Successfully created historic exchange rates ({} objects)'.format(str(counter))
        }
        return response_object
