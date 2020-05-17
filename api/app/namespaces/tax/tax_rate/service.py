from datetime import date

from .model import TaxRate
from ...country import Country



class TaxRateService:
    @staticmethod
    def get_by_tax_code_country_tax_date(tax_code_code: str, country: Country, tax_date: date) -> TaxRate:
        tax_rate: TaxRate = TaxRate.query.filter(TaxRate.tax_code==tax_code_code, TaxRate.country==country, TaxRate.valid_from<=tax_date, TaxRate.valid_to>=tax_date).first()
        if tax_rate:
            return tax_rate
        else:
            raise NotFound('The tax rate for the tax code: "{}" and the country: "{}" could not be found. Please get in contact with one of the admins.'.format(tax_code, country.name))

    @staticmethod
    def get_by_tax_rate_type_country_tax_date(country: Country, tax_rate_type_name: str, tax_date: date) -> TaxRate:
        tax_rate: TaxRate = TaxRate.query.filter(TaxRate.country==country, TaxRate.tax_rate_type_name==tax_rate_type_name, TaxRate.valid_from<=tax_date, TaxRate.valid_to>=tax_date).first()
        if tax_rate:
            return tax_rate
        else:
            raise NotFound('The tax rate for the tax rate type "{}" and the country "{}" could not be found. Please get in contact with one of the admins.'.format(tax_rate_type_name, country.name))
