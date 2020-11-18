from datetime import datetime
from flask_script import Command
from werkzeug.exceptions import InternalServerError
from typing import List, Dict

from app.extensions import db


from app.namespaces.currency import Currency
from app.namespaces.country import EU, Country
from app.namespaces.transaction_type import TransactionType
from app.namespaces.tax.tax_code import TaxCode
from app.namespaces.tax.tax_treatment import TaxTreatment
from app.namespaces.tax.vat import Vat
from app.namespaces.tax.vat_threshold import VatThreshold
from app.namespaces.tax.tax_rate_type import TaxRateType
from app.namespaces.platform import Platform
from app.namespaces.channel import Channel
from app.namespaces.tag import Tag


from .seeds.currencies import currencies
from .seeds.eu import EUSeedService
from .seeds.countries import CountrySeedService
from .seeds.tax_codes import TaxCodesSeedService
from .seeds.tax_rate_types import tax_rate_types
from .seeds.vats import VatSeedService
from .seeds.vat_thresholds import VatThresholdSeedService
from .seeds.transaction_types import transaction_types
from .seeds.transaction_types_public import TransactionTypePublicSeedService
from .seeds.tax_treatments import tax_treatments, TaxTreatmentSeedService
from .seeds.exchange_rates import ExchangeRatesSeedService
from .seeds.platforms import platforms, PlatformSeedService
from .seeds.channels import channels
from .seeds.accounting_firms import AccountingFirmSeedService
from .seeds.sample_seller_firm import SellerFirmSeedService, SampleFirmInformationSeedService, VATINSeedService
from .seeds.users import AdminSeedService, TaxAuditorSeedService, SellerSeedService
from .seeds.tags import tags

countries = CountrySeedService.seed_countries()
eu = EUSeedService.seed_eu()
tax_codes = TaxCodesSeedService.seed_tax_codes()


things_list = {
    'currencies': [Currency, currencies],
    'eu': [EU, eu],
    'countries': [Country, countries],
    'tax_codes': [TaxCode, tax_codes],
    'tax_rate_types': [TaxRateType, tax_rate_types],
    'transaction_types': [TransactionType, transaction_types],
    'tax_treatments': [TaxTreatment, tax_treatments],
    'platforms': [Platform, platforms],
    'channels': [Channel, channels],
    'tags': [Tag, tags]
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
            PlatformSeedService.append_channels_to_platform()

            db.session.commit()

            print('Creating Vat Rates...')
            response_object_vat_rates = VatSeedService.seed_tax_rates()
            response_objects.append(response_object_vat_rates)

            print('Creating Exchange Rates...')
            response_object_exchange_rates = ExchangeRatesSeedService.create_historic_exchange_rates()
            response_objects.append(response_object_exchange_rates)

            print('Creating Vat Thresholds...')
            response_object_vat_thresholds = VatThresholdSeedService.seed_vat_thresholds()
            response_objects.append(response_object_vat_thresholds)

            print('Creating Public Transaction Types...')
            response_object_transaction_types_public = TransactionTypePublicSeedService.seed_transaction_types_public()
            response_objects.append(response_object_transaction_types_public)

            print('Preparing Sample Seller Firm Showcase...')
            print('...Sample Seller Firm')
            SellerFirmSeedService.seed_sample_seller_firm()
            print('...Sample Seller')
            SellerSeedService.seed_seller()
            print('...Append Seller To Firm')
            SellerSeedService.append_seller_firm_to_seller()
            print('...Seller Firm Static Data')
            SampleFirmInformationSeedService.seed_sample_data_static()
            print('...arrival vat numbers')
            VATINSeedService.seed_bond_transaction_vatins()
            print('...Seller Firm Transaction Data')
            SampleFirmInformationSeedService.seed_sample_transaction_input_data()


            for response_object in response_objects:
                print("")
                for key, val in response_object.items():
                    print(key, ':', val)


            time_end = datetime.utcnow()
            lengths = time_end - time_start

            print("")
            print("DB successfully seeded in {}.".format(str(lengths)))



# class SeedCommandTest():
#     def run(self):
#         time_start = datetime.utcnow()
#         print("Dropping tables...")
#         db.drop_all()
#         db.create_all()

#         print('Seeding things...')
#         response_objects = SeedService.seed_things(things_list)

#         print('Seeding businesses...')
#         AccountingFirmSeedService.seed_accounting_firm()

#         print('Seeding users...')
#         AdminSeedService.seed_admin()
#         TaxAuditorSeedService.seed_tax_auditor()

#         print('Appending Transaction Types to Tax Treatments...')
#         TaxTreatmentSeedService.append_transaction_types_to_tax_treatments()

#         print('Appending Countries to EU...')
#         EUSeedService.append_countries_to_eu()

#         print('Appending Users to Businesses...')
#         AccountingFirmSeedService.append_tax_auditor_to_accounting_firm()
#         AdminSeedService.append_accounting_firm_to_admin()

#         print('Appending Channels to Platforms...')
#         PlatformSeedService.append_channels_to_platform()

#         db.session.commit()

#         print('Creating Vat Rates...')
#         response_object_vat_rates = VatSeedService.seed_tax_rates()
#         response_objects.append(response_object_vat_rates)

#         print('Creating Exchange Rates...')
#         response_object_exchange_rates = ExchangeRatesSeedService.create_historic_exchange_rates()

#         response_objects.append(response_object_exchange_rates)

#         for response_object in response_objects:
#             print("")
#             for key, val in response_object.items():
#                 print(key, ':', val)

#         time_end = datetime.utcnow()
#         lengths = time_end - time_start

#         print("")
#         print("DB successfully seeded in {}.".format(str(lengths)))
