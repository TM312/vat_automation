from datetime import datetime
from flask_script import Command
from werkzeug.exceptions import InternalServerError

from app.extensions import db


from app.namespaces.currency import Currencys
from app.namespaces.country import EU, Country
from app.namespaces.transaction import TransactionType
from app.namespaces.tax import TaxTreatment, TaxCode, TaxRate, TaxRateType
from app.namespaces.platform import Amazon
from app.namespaces.channel import Channel
from app.namespaces.customer import CustomerRelationship
from app.namespaces.user import Admin, TaxAuditor
from app.namespaces.business import AccountingFirm


from .seeds.currencies import currencies
from .seeds.eu import eu, EUSeedService
from .seeds.countries import countries
from .seeds.tax_codes import tax_codes
from .seeds.tax_rate_types import tax_rate_types
from .seeds.tax_rates import tax_rates
from .seeds.transaction_types import transaction_types
from .seeds.tax_treatments import tax_treatments, TaxTreatmentSeedService
from .seeds.exchange_rates import ExchangeRatesSeedService
from .seeds.platforms import platforms
from .seeds.channels import channels
from .seeds.customer_relationships import customer_relationships
from .seeds.users import admins, tax_auditors
from .seeds.accounting_firms import accounting_firms


things_list = {
    'currencies': [Currency, currencies],
    'eu': [EU, eu],
    'countries': [Country, countries],
    'tax_codes': [TaxCode, tax_codes],
    'tax_rate_types': [TaxRateType, tax_rate_types],
    'tax_rates': [TaxRate, tax_rates],
    'transaction_types': [TransactionType, transaction_types],
    'tax_treatments': [TaxTreatment, tax_treatments],
    'platforms': [Amazon, platforms],
    'channels': [Channel, channels],
    'customer_relationships': [CustomerRelationship, customer_relationships],
    'admins': [Admin, admins],
    'accounting_firms': [AccountingFirm, accounting_firms],
    'tax_auditors': [TaxAuditor, tax_auditors],

}

class SeedService:
    @staticmethod
    def seed_things(things_list: dict) -> list:

        response_objects = []

        for key, val in things_list.items():
            response_object = SeedService.seed_thing(key, klass=val[0], object_dict=val[1])
            response_objects.append(response_object)

        return response_objects


    @staticmethod
    def seed_thing(key:str, klass, object_dict: dict) -> dict:
        try:
            db.session.bulk_insert_mappings(klass, object_dict)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully seeded {} ({} objects).'.format(key, len(object_dict.items()))
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
            time_start = datetime.utcnow()
            print("Dropping tables...")
            db.drop_all()
            db.create_all()
            response_objects = SeedService.seed_things()

            EUSeedService.append_countries_to_eu()
            TaxTreatmentSeedService.append_transaction_types_to_tax_treatments()

            db.session.commit()

            response_object_exchange_rates = ExchangeRatesSeedService.create_exchange_rate_collections()

            response_objects.append(response_object_exchange_rates)

            for response_object in response_objects:
                for key, val in response_object.items():
                    print(key, ':', val)
                    print("")

            time_end = datetime.utcnow()
            lengths = time_end - time_start

            print("DB successfully seeded in {}.".format(str(lengths)))
