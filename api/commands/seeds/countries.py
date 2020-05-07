#source: https://en.wikipedia.org/wiki/VAT_identification_number, 2020-05-05

import pandas as pd
from os import path
from current_app.config import BASE_PATH_SEEDS

file = 'countries.csv'

dirpath = path.join(
    BASE_PATH_SEEDS,
    file)


df = pd.read_csv(dirpath)
countries = df.to_dict('records')
