#source: https://en.wikipedia.org/wiki/VAT_identification_number, 2020-05-05

import pandas as pd
from os import path


class CountrySeedService:

    @staticmethod
    def seed_countries():
        from . import BASE_PATH_SEEDS
        from . import TAX_DEFAULT_VALIDITY
        from . import SERVICE_START_DATE
        file = 'countries.csv'

        dirpath = path.join(
            BASE_PATH_SEEDS,
            file)

        df = pd.read_csv(dirpath)
        # https://stackoverflow.com/questions/26033301/make-pandas-dataframe-to-a-dict-and-dropna

        countries = []
        countries_pre = [ {k:v for k,v in m.items() if pd.notnull(v)} for m in df.to_dict(orient='rows')]
        countries_validity = { 'valid_from': SERVICE_START_DATE, 'valid_to': TAX_DEFAULT_VALIDITY }
        for country in countries_pre:
            country.update(countries_validity)
            countries.append(country)
        return countries


        return countries
