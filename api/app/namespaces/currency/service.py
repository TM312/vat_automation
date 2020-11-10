from typing import List
from app.extensions import db
from flask import current_app

from . import Currency
from .interface import CurrencyInterface

from werkzeug.exceptions import InternalServerError


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
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.warning('Exception in Currency Update: {}'.format(e))
                db.session.rollback()
                raise InternalServerError

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
