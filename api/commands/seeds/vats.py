from os import path
import pandas as pd
from datetime import datetime
from app.extensions import db
from app.namespaces.tax.vat.service import VatService



file_rates = 'vat.csv'
file_rates_covid19 = 'vat_covid19.csv'
file_types = 'tax_rate_types.csv'


class VatSeedService:

    @staticmethod
    def seed_tax_rates():
        from . import BASE_PATH_SEEDS
        from . import SERVICE_START_DATE
        # from . import TAX_DEFAULT_VALIDITY

        dirpath_rates = path.join(BASE_PATH_SEEDS, file_rates)
        dirpath_types = path.join(BASE_PATH_SEEDS, file_types)
        df_rates = pd.read_csv(dirpath_rates)

        df_types = pd.read_csv(dirpath_types)

        tax_rates = []
        # counter = 0

        countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU',
                    'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'GB']

        for country in countries:
            for i, tax_code_row in enumerate(range(len(df_types.index))):
                # counter += 1
                tax_code = df_types.iloc[tax_code_row]['tax_code']
                tax_rate_type_code = df_types.loc[df_types['tax_code'] == tax_code][country].iloc[0]
                rate = df_rates.loc[df_rates['country_code'] == country].loc[df_rates['tax_rate_type_code'] == tax_rate_type_code].iloc[0]['rate']

                vat_data = {
                    'valid_from': SERVICE_START_DATE,
                    # 'valid_to': TAX_DEFAULT_VALIDITY,
                    'country_code': country,
                    'tax_code_code': tax_code,
                    'tax_rate_type_code': tax_rate_type_code,
                    'rate': rate
                }

                try:
                    VatService.create(vat_data)
                except:
                    db.session.rollback()
                    raise

        # dirpath_rates_covid19 = path.join(BASE_PATH_SEEDS, file_rates_covid19)
        # df_rates_covid19 = pd.read_csv(dirpath_rates_covid19)

        # vats = VatService.get_by_country_tax_rate_type(country_code, tax_rate_type_code)
        # for vat in vats:

        #     valid_from=vat_data.get('valid_from'),
        #     valid_to=vat_data.get('valid_to'),
        #     country_code=vat_data.get('country_code'),
        #     tax_code_code=vat_data.get('tax_code_code'),
        #     tax_rate_type_code=vat_data.get('tax_rate_type_code'),
        #     comment = '',
        #     rate=vat_data.get('rate')


        #     vat.update(data_changes)

        # rate_covid19 = df_rates_covid19.loc[df_rates_covid19['country_code'] == country].loc[df_rates_covid19['tax_rate_type_code'] == tax_rate_type_code].iloc[0]['rate']
        # valid_from_covid19 = df_rates_covid19.loc[df_rates_covid19['country_code'] == country].loc[df_rates_covid19['tax_rate_type_code'] == tax_rate_type_code].iloc[0]['valid_from']
        # valid_to_covid19 = df_rates_covid19.loc[df_rates_covid19['country_code'] == country].loc[df_rates_covid19['tax_rate_type_code'] == tax_rate_type_code].iloc[0]['valid_to']

        # vat_data = {
        #     'valid_from': valid_from_covid19,
        #     'valid_to': valid_to_covid19,
        #     'country_code': country,
        #     'tax_code_code': tax_code,
        #     'tax_rate_type_code': tax_rate_type_code,
        #     'rate': rate_covid19
        # }

        # try:
        #     VatService.create(vat_data)
        # except:
        #     db.session.rollback()
        #     raise


        response_object = {
            'status': 'success',
            'message': 'Successfully created vat rates ({} objects)'.format(str(i+1))
        }

        return response_object
