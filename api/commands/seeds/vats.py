from os import path
import pandas as pd
from datetime import datetime
from app.namespaces.tax.vat.service import VatService

from flask import current_app


file_rates = 'vat.csv'
file_types = 'tax_rate_types.csv'


class VatSeedService:

    @staticmethod
    def seed_tax_rates():
        from . import BASE_PATH_SEEDS
        from . import SERVICE_START_DATE
        from . import TAX_DEFAULT_VALIDITY

        dirpath_rates = path.join(BASE_PATH_SEEDS, file_rates)
        dirpath_types = path.join(BASE_PATH_SEEDS, file_types)
        df_rates = pd.read_csv(dirpath_rates)
        df_types = pd.read_csv(dirpath_types)

        tax_rates = []
        counter = 0

        countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU',
                    'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'GB']

        for country in countries:
            for tax_code_row in range(len(df_types.index)):
                counter += 1
                tax_code = df_types.iloc[tax_code_row]['tax_code']
                tax_rate_type_code = df_types.loc[df_types['tax_code'] == tax_code][country].iloc[0]
                rate = df_rates.loc[df_rates['country_code'] == country].loc[df_rates['tax_rate_type_code'] == tax_rate_type_code].iloc[0]['rate']


                vat_data = {
                    'valid_from': SERVICE_START_DATE,
                    'valid_to': TAX_DEFAULT_VALIDITY,
                    'country_code': country,
                    'tax_code_code': tax_code,
                    'tax_rate_type_code': tax_rate_type_code,
                    'rate': rate
                }

                VatService.create(vat_data)

                # tax_rates.append(vat)

        response_object = {
            'status': 'success',
            'message': 'Successfully created vat rates ({} objects)'.format(str(counter))
        }

        return response_object
