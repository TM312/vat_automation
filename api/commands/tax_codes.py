import pandas as pd


file = '/Users/tm/Projects/NTAMAZON/webapp/api/commands/tax_codes.csv'
df = pd.read_csv(file)

tax_codes = df.to_dict('records')
