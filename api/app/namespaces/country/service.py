from .model import Country, EU

from werkzeug.exceptions import NotFound


class CountryService:
    @staticmethod
    def get_by_code(country_code: str) -> Country:
        country = Country.query.filter_by(code=country_code).first()
        if country:
            return country
        else:
            raise NotFound(
                'The country "{}" is currently not supported by our database. Please get in contact with one of the admins.'.format(country_code))

    @staticmethod
    def get_eu_by_date(date) -> EU:
        eu = EU.query.filter(EU.valid_from <= date,
                             EU.valid_to >= date).first()
        if eu:
            return eu
        else:
            raise NotFound(
                'A constellation of EU countries has not been defined for the requested date ({})'.format(str(date)))
