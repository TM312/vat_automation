from os import path
import pandas as pd
from datetime import datetime

from flask import current_app

BASE_PATH_SEEDS = current_app.config["BASE_PATH_SEEDS"]
SERVICE_START_DATE = current_app.config["SERVICE_START_DATE"]


file_rates = 'tax_rates.csv'
file_types = 'tax_rate_types.csv'

dirpath_rates = path.join(
    BASE_PATH_SEEDS,
    file_rates)

dirpath_types = path.join(
    BASE_PATH_SEEDS,
    file_types)


df_rates = pd.read_csv(dirpath_rates)
df_types = pd.read_csv(dirpath_types)



def get_tax_rates(df_rates, df_types):
    tax_rates = []

    countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU',
                 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'GB']

    for country in countries:
        print(country)
        for tax_code_row in range(len(df_types.index)):
            tax_code = df_types.iloc[tax_code_row]['tax_code']
            tax_rate_type_code = df_types.loc[df_types['tax_code']
                                         == tax_code][country].iloc[0]
            rate = df_rates.loc[df_rates['country_code'] ==
                                country].loc[df_rates['tax_rate_type_code'] == tax_rate_type_code].iloc[0]['rate']

            # print(country)
            # print(tax_code)
            # print(tax_rate_type)
            # print(rate)

            tax_rate = {
                'valid_from': SERVICE_START_DATE,
                'country_code': country,
                'tax_rate_type_code': tax_rate_type_code,
                'rate': rate
            }
            tax_rates.append(tax_rate)

    return tax_rates


tax_rates = get_tax_rates(df_rates, df_types)
