from datetime import date
from werkzeug.exceptions import NotFound

from .model import Vat
from ...country import Country




class VatService:
    @staticmethod
    def get_by_tax_code_country_tax_date(tax_code_code: str, country: Country, tax_date: date) -> Vat:
        vat: Vat = Vat.query.filter(Vat.tax_code==tax_code_code, Vat.country==country, Vat.valid_from<=tax_date, Vat.valid_to>=tax_date).first()
        if vat:
            return vat
        else:
            raise NotFound('The tax rate for the tax code: "{}" and the country: "{}" could not be found. Please get in contact with one of the admins.'.format(tax_code, country.name))

    @staticmethod
    def get_by_tax_rate_type_country_tax_date(country: Country, tax_rate_type_code: str, tax_date: date) -> Vat:
        vat: Vat = Vat.query.filter(Vat.country==country, Vat.tax_rate_type_code==tax_rate_type_code, Vat.valid_from<=tax_date, Vat.valid_to>=tax_date).first()
        if vat:
            return vat
        else:
            raise NotFound('The tax rate for the tax rate type "{}" and the country "{}" could not be found. Please get in contact with one of the admins.'.format(tax_rate_type_code, country.name))
