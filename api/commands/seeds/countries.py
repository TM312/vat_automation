#source: https://en.wikipedia.org/wiki/VAT_identification_number, 2020-05-05

import pandas as pd
from os import path


class CountrySeedService:

    @staticmethod
    def seed_countries():
        from . import BASE_PATH_SEEDS
        file = 'countries.csv'

        dirpath = path.join(
            BASE_PATH_SEEDS,
            file)

        df = pd.read_csv(dirpath)
        # https://stackoverflow.com/questions/26033301/make-pandas-dataframe-to-a-dict-and-dropna
        countries = [ {k:v for k,v in m.items() if pd.notnull(v)} for m in df.to_dict(orient='rows')]
        # countries = df.to_dict('records')
        return countries
