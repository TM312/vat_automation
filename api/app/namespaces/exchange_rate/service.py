from typing import List, Dict
from flask import current_app

from . import ExchangeRate
from .interface import ExchangeRateInterface

from werkzeug.exceptions import InternalServerError, NotFound

from datetime import datetime, date
from app.extensions import db



class ExchangeRateService:
    @staticmethod
    def get_all() -> List[ExchangeRate]:
        exchange_rates = ExchangeRate.query.all()
        return exchange_rates

    @staticmethod
    def get_by_id(exchange_rate_id: int) -> ExchangeRate:
        return ExchangeRate.query.filter_by(id = exchange_rate_id).first()

    @staticmethod
    def get_by_base_target_date(base: str, target: str, date: date) -> ExchangeRate:
        return ExchangeRate.query.filter(
            ExchangeRate.base==base,
            ExchangeRate.target==target,
            ExchangeRate.date==date
            ).first()

    @staticmethod
    def get_list_by_base_date(base: str, date: date) -> List[ExchangeRate]:
        return ExchangeRate.query.filter(
            ExchangeRate.date == date,
            ExchangeRate.base == base
            ).all()


    @staticmethod
    def update(exchange_rate_id: int, data_changes: ExchangeRateInterface) -> ExchangeRate:
        exchange_rate = ExchangeRateService.get_by_id(exchange_rate_id)
        exchange_rate.update(data_changes)
        db.session.commit()
        return exchange_rate

    @staticmethod
    def delete_by_id(exchange_rate_id: str):
        exchange_rate = ExchangeRateService.get_by_id(exchange_rate_id)
        if exchange_rate:
            db.session.delete(exchange_rate)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'ExchangeRate (id: {}) has been successfully deleted.'.format(exchange_rate_id)
            }
            return response_object
        else:
            raise NotFound('This exchange_rate does not exist.')


    @staticmethod
    def create(exchange_rate_data: ExchangeRateInterface) -> ExchangeRate:
        new_exchange_rate = ExchangeRate(
            source = exchange_rate_data.get('source'),
            created_on = exchange_rate_data.get('created_on'),
            date = exchange_rate_data.get('date'),
            base = exchange_rate_data.get('base'),
            target = exchange_rate_data.get('target'),
            rate = exchange_rate_data.get('rate')
        )

        db.session.add(new_exchange_rate)
        db.session.commit()

        return new_exchange_rate


    @staticmethod
    def create_between_rate(date: date, base: str, target: str) -> ExchangeRate:
        rate_base_eur = ExchangeRateService.get_by_base_target_date(base, 'EUR', date).rate
        rate_eur_target = ExchangeRateService.get_by_base_target_date('EUR', target, date).rate

        rate_base_target = rate_base_eur * rate_eur_target

        exchange_rate_data = {
            'source': 'ECB',
            'date': date,
            'base': base,
            'target': target,
            'rate': round(float(rate_base_target), 5)
        }
        ExchangeRateService.create(exchange_rate_data)



    @staticmethod
    def process_ecb_rates(date, exchange_rate_dict: Dict, supported_currencies: List[str]) -> None:
        import more_itertools as mit

        for currency_code in supported_currencies:
            value = exchange_rate_dict[currency_code]

            exchange_rate_data = {
                'source': 'ECB',
                'date': date,
                'base': 'EUR',
                'target': currency_code,
                'rate': round(float(value), 5)
            }

            ExchangeRateService.create(exchange_rate_data)

            # creating reverse rates
            exchange_rate_data['base'] = currency_code
            exchange_rate_data['target'] = 'EUR'
            exchange_rate_data['rate'] = round(1/float(value), 5)

            ExchangeRateService.create(exchange_rate_data)


        currency_tuples = list(mit.distinct_combinations(supported_currencies, 2))
        for currency_tuple in currency_tuples:
            ExchangeRateService.create_between_rate(date, base=currency_tuple[0], target=currency_tuple[1])





    @staticmethod
    def retrieve_ecb_exchange_rates():
        exchange_rate_dict = {}

        #get exchange rate data
        import requests
        r = requests.get('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml', stream=True)
        from xml.etree import ElementTree as ET
        tree = ET.parse(r.raw)
        root = tree.getroot()
        namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):
            # data is added to dict
            exchange_rate_dict[str(cube.attrib['currency'])] = cube.attrib['rate']
        return exchange_rate_dict
