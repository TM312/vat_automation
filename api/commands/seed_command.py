from datetime import datetime
from flask_script import Command
from werkzeug.exceptions import InternalServerError
from typing import List, Dict

from app.extensions import db


from app.namespaces.currency.model import Currency
from app.namespaces.country.model import EU, Country
from app.namespaces.transaction.model import TransactionType
from app.namespaces.tax.tax_code.model import TaxCode
from app.namespaces.tax.tax_treatment.model import TaxTreatment
from app.namespaces.tax.vat.model import Vat, TaxRateType
from app.namespaces.platform.amazon.model import Amazon
from app.namespaces.channel.model import Channel
#from app.namespaces.user.admin.model import Admin
#from app.namespaces.user.tax_auditor.model import TaxAuditor
#from app.namespaces.business.accounting_firm.model import AccountingFirm


from .seeds.currencies import currencies
from .seeds.eu import EUSeedService
from .seeds.countries import CountrySeedService
from .seeds.tax_codes import TaxCodesSeedService
from .seeds.tax_rate_types import tax_rate_types
from .seeds.vats import VatSeedService
from .seeds.transaction_types import transaction_types
from .seeds.tax_treatments import tax_treatments, TaxTreatmentSeedService
from .seeds.exchange_rates import ExchangeRatesSeedService
from .seeds.platforms import platforms, PlatformSeedService
from .seeds.channels import channels
#from .seeds.users import tax_auditors#, admins
from .seeds.accounting_firms import AccountingFirmSeedService
from .seeds.users import AdminSeedService, TaxAuditorSeedService

countries = CountrySeedService.seed_countries()
eu = EUSeedService.seed_eu()
tax_codes = TaxCodesSeedService.seed_tax_codes()
tax_rates = VatSeedService.seed_tax_rates()


things_list = {
    'currencies': [Currency, currencies],
    'eu': [EU, eu],
    'countries': [Country, countries],
    'tax_codes': [TaxCode, tax_codes],
    'tax_rate_types': [TaxRateType, tax_rate_types],
    'tax_rates': [Vat, tax_rates],
    'transaction_types': [TransactionType, transaction_types],
    'tax_treatments': [TaxTreatment, tax_treatments],
    'platforms': [Amazon, platforms],
    'channels': [Channel, channels],
#    'admins': [Admin, admins],
    #'accounting_firms': [AccountingFirm, accounting_firms],
    #'tax_auditors': [TaxAuditor, tax_auditors],

}

class SeedService:
    @staticmethod
    def seed_things(things_list: Dict) -> List[Dict]:

        response_objects = []

        for key, val in things_list.items():
            klass = val[0]
            object_dict_list = val[1]
            db.session.bulk_insert_mappings(klass, object_dict_list)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully seeded {} ({} objects).'.format(key, len(object_dict_list))
            }
            response_objects.append(response_object)

        return response_objects


    # @staticmethod
    # def seed_thing(key:str, klass, object_dict: Dict) -> Dict:
    #     try:
    #         db.session.bulk_insert_mappings(klass, object_dict)
    #         db.session.commit()
    #         response_object = {
    #             'status': 'success',
    #             'message': 'Successfully seeded {} ({} objects).'.format(key, len(object_dict.items()))
    #         }
    #         return response_object
    #     except:
    #         db.session.rollback()
    #         raise InternalServerError('Error seeding {}'.format(key))



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

            print('Seeding things...')
            response_objects = SeedService.seed_things(things_list)

            print('Seeding businesses...')
            AccountingFirmSeedService.seed_accounting_firm()

            print('Seeding users...')
            AdminSeedService.seed_admin()
            TaxAuditorSeedService.seed_tax_auditor()


            print('Appending Transaction Types to Tax Treatments...')
            TaxTreatmentSeedService.append_transaction_types_to_tax_treatments()

            print('Appending Countries to EU...')
            EUSeedService.append_countries_to_eu()

            print('Appending Users to Businesses...')
            AccountingFirmSeedService.append_tax_auditor_to_accounting_firm()
            AdminSeedService.append_accounting_firm_to_admin()

            print('Appending Channels to Platforms...')
            print('... mfn, afn to Amazon...')
            PlatformSeedService.append_channels_to_platform()

            db.session.commit()

            print('Creating Exchange Rates...')
            response_object_exchange_rates = ExchangeRatesSeedService.create_exchange_rate_collections()

            response_objects.append(response_object_exchange_rates)

            for response_object in response_objects:
                print("")
                for key, val in response_object.items():
                    print(key, ':', val)


            time_end = datetime.utcnow()
            lengths = time_end - time_start

            print("")
            print("DB successfully seeded in {}.".format(str(lengths)))
