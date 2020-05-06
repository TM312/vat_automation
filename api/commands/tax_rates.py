from datetime import datetime

import pandas as pd
from datetime import datetime


file_rates = '/Users/tm/Projects/NTAMAZON/webapp/api/commands/tax_rates.csv'
file_types = '/Users/tm/Projects/NTAMAZON/webapp/api/commands/tax_rate_types.csv'


df_rates = pd.read_csv(file_rates)
df_types = pd.read_csv(file_types)


def get_tax_rates(df_rates, df_types):
    tax_rates = []

    countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU',
                 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'GB']

    for country in countries:
        print(country)
        for tax_code_row in range(len(df_types.index)):
            tax_code = df_types.iloc[tax_code_row]['tax_code']
            tax_rate_type = df_types.loc[df_types['tax_code']
                                         == tax_code][country].iloc[0]
            rate = df_rates.loc[df_rates['country_code'] ==
                                country].loc[df_rates['tax_rate_type_code'] == tax_rate_type].iloc[0]['rate']

            # print(country)
            # print(tax_code)
            # print(tax_rate_type)
            # print(rate)

            tax_rate = {
                'valid_from': datetime.strptime('01-06-2018', '%d-%m-%Y').date(),
                'country_code': country,
                'tax_rate_type_code': tax_rate_type_code,
                'rate': rate
            }
            tax_rates.append(tax_rate)

    return tax_rates


tax_rates = get_tax_rates(df_rates, df_types)
