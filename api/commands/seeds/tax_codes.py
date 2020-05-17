import pandas as pd
from os import path
from flask import current_app

file = 'tax_codes.csv'

class TaxCodesSeedService:

    @staticmethod
    def seed_tax_codes():
        BASE_PATH_SEEDS = current_app.config["BASE_PATH_SEEDS"]

        dirpath = path.join(BASE_PATH_SEEDS, file)
        df = pd.read_csv(dirpath)

        tax_codes = df.to_dict('records')
        return tax_codes
