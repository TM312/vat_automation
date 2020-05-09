import pandas as pd
from os import path
from flask import current_app

BASE_PATH_SEEDS = current_app.config["BASE_PATH_SEEDS"]

file = 'tax_codes.csv'

dirpath = path.join(
    BASE_PATH_SEEDS,
    file)

df = pd.read_csv(dirpath)

tax_codes = df.to_dict('records')
