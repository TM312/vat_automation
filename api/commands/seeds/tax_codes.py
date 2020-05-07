import pandas as pd
from os import path
from current_app.config import BASE_PATH_SEEDS

file = 'tax_codes.csv'

dirpath = path.join(
    BASE_PATH_SEEDS,
    file)

df = pd.read_csv(dirpath)

tax_codes = df.to_dict('records')
