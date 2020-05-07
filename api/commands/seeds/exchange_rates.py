
from current_app.config import BASE_PATH_SEEDS
from os import path
from app.namespaces.exchange_rates.service import ExchangeRateService
from app.namespaces.exchange_rates.model import ExchangeRatesEUR
from werkzeug.exceptions import UnsupportedMediaType, InternalServerError

import pandas as pd

file = 'hist_exchange_rates.csv'
dirpath = path.join(
    BASE_PATH_SEEDS,
    file)

df = pd.read_csv(dirpath)


class ExchangeRatesSeedService:
    @staticmethod
    def get_date_or_None_incl_format(df, i: int, column: str, dstr_format:str, alternative_dstr_format) -> date or None:
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
    def create_exchange_rate_collections():
        for row in range(len(df.index)):
            date = get_date_or_None_incl_format(df, i=row, column='Date', dstr_format='%Y-%m-%d', alternative_dstr_format='%Y.%m.%d')
            if not date:
                raise InternalServerError
            else:
                exchange_rate_collection = ExchangeRateService.create_exchange_rate_collection(date)

                exchange_rates_EUR = ExchangeRatesEUR(
                    source='ECB',
                    created_on=datetime.utcnow(),
                    date=date,
                    exchange_rate_collection_id=exchange_rate_collection.id,
                    eur=1.0000,
                    gbp=df.iloc[row]['GBP'],
                    czk=df.iloc[row]['CZK'],
                    pln=df.iloc[row]['PLN']
                )

                #add exchange_rate_collection to db
                db.session.add(exchange_rates_EUR)
                db.session.commit()

                try:
                    ExchangeRateService.create_exchange_rates_GBP(date)
                    ExchangeRateService.create_exchange_rates_CZK(date)
                    ExchangeRateService.create_exchange_rates_PLN(date)

                    response_object = {
                        'status': 'success',
                        'message': 'Successfully seeded.'
                    }
                    return response_object

                except:
                    response_object = {
                        'status': 'error',
                        'message': 'Failed to create GBP CZK PLN exchange rates.'
                    }
                    raise InternalServerError(response_object)


            else:
                response_object = {
                    'status': 'error',
                    'message': 'The corresponding exchange rate collection can not be found.'
                }
                raise InternalServerError(response_object)
