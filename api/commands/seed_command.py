from datetime import datetime
from flask_script import Command
from werkzeug.exceptions import InternalServerError

from app.extensions import db


from app.namespaces.currency.model import Currency
from app.namespaces.country.model import EU
from app.namespaces.country.model import Country
from app.namespaces.tax.tax_code.model import TaxCode
from app.namespaces.tax.tax_rate.model import TaxRate, TaxRateType
from app.namespaces.transaction.model import TaxRate, TaxRateType


#from app.exchange_rates import ExchangeRateCollection

from .currencies import currencies,
from .eu import eu, EUSeedService
from .countries import countries,
from .tax_codes import tax_codes
from .tax_rate_types import tax_rate_types
from .tax_rates import tax_rates
from .transaction_types import transaction_types

things_list = {
    'currencies': [Currency, currencies],
    'eu': [EU, eu],
    'countries': [Country, countries],
    'tax_codes': [TaxCode, tax_codes],
    'tax_rate_types': [TaxRateType, tax_rate_types],
    'tax_rates': [TaxRate, tax_rates],
    'transaction_types': [TransactionType, transaction_types],
}

class SeedService:

    @staticmethod
    def seed_things(things_list: dict):

        response_objects = []

        for key, val in things_list.items():
            response_object = SeedService.seed_thing(key, val[0], val[1])
            response_objects.append(response_object)

        return response_objects


    @staticmethod
    def seed_thing(key, klass, object_dict: dict):
        try:
            db.session.bulk_insert_mappings(klass, object_dict)
            response_object = {
                'status': 'success',
                'message': 'Successfully seeded {}.'.format(key)
            }
            return response_object
        except:
            db.session.rollback()
            raise InternalServerError('Error seeding currencies')



class SeedCommand(Command):
    """ Seed the DB."""

    def run(self):
        if (
            input(
                "Are you sure you want to drop all tables and recreate? (y/N)\n"
            ).lower()
            == "y"
        ):
            print("Dropping tables...")
            db.drop_all()
            db.create_all()
            response_objects = SeedService.seed_things()
            db.session.commit()
            for response_object in response_objects:
                for key in response_object[key]:
                    print(str(key), ':', str(response_object[key]))
            print("DB successfully seeded.")
