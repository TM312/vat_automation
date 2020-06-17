from datetime import date
from typing import List

from app.extensions import db
from werkzeug.exceptions import NotFound

from .interface import CountryInterface
from . import Country, EU


class CountryService:
    @staticmethod
    def get_all() -> List[Country]:
        countries = Country.query.all()
        return countries

    @staticmethod
    def get_by_code(country_code: str) -> Country:
        country = Country.query.filter_by(code=country_code).first()
        if country:
            return country
        else:
            raise NotFound(
                'The country "{}" is currently not supported by our database. Please get in contact with one of the admins.'.format(country_code))

    @staticmethod
    def get_eu_by_date(date: date) -> EU:
        eu = EU.query.filter(EU.valid_from <= date,
                             EU.valid_to >= date).first()
        if eu:
            return eu
        else:
            raise NotFound('A constellation of EU countries has not been defined for the requested date ({})'.format(str(date)))



    @staticmethod
    def update(code: str, data_changes: CountryInterface) -> Country:
        country = CountryService.get_by_code(code)
        country.update(data_changes)
        db.session.commit()
        return country

    @staticmethod
    def delete_by_code(code: str):
        country = Country.query.filter(Country.code == code).first()
        if country:
            db.session.delete(country)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Country (code: {}) has been successfully deleted.'.format(code)
            }
            return response_object
        else:
            raise NotFound('This country does not exist.')

    @staticmethod
    def create(country_data: CountryInterface) -> Country:

        new_country = Country(
            code = country_data.get('code'),
            vat_country_code = country_data.get('vat_country_code'),
            name = country_data.get('name'),
            valid_from = country_data.get('valid_from'),
            valid_to = country_data.get('valid_to'),
            currency_code = country_data.get('currency_code')
        )

        #add seller firm to db
        db.session.add(new_country)
        db.session.commit()

        return new_country
