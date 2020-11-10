from typing import List
from app.extensions import db


from . import Currency
from .interface import CurrencyInterface


class CurrencyService:
    @staticmethod
    def get_all() -> List[Currency]:
        currencies = Currency.query.all()
        return currencies

    @staticmethod
    def get_by_code(code: str) -> Currency:
        return Currency.query.filter_by(code = code).first()

    @staticmethod
    def update(code: str, data_changes: CurrencyInterface) -> Currency:
        currency = CurrencyService.get_by_code(code)
        if isinstance(currency, Currency):
            currency.update(data_changes)
            db.session.commit()
            return currency

    @staticmethod
    def delete_by_code(code: str):
        currency = CurrencyService.get_by_code(code)
        if currency:
            db.session.delete(currency)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Currency (code: {}) has been successfully deleted.'.format(code)
            }
            return response_object
        else:
            raise NotFound('This currency does not exist.')

    @staticmethod
    def create(currency_data: CurrencyInterface) -> Currency:

        new_currency = Currency(
            code=currency_data.get('code'),
            name=currency_data.get('name')
        )

        #add seller firm to db
        db.session.add(new_currency)
        db.session.commit()

        return new_currency
