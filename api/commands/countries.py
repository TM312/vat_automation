#source: https://en.wikipedia.org/wiki/VAT_identification_number, 2020-05-05
import pandas as pd


file = '/Users/tm/Projects/NTAMAZON/webapp/api/commands/countries.csv'
df = pd.read_csv(file)

countries = df.to_dict('records')
