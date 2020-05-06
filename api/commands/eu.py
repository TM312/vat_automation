#source: https: // en.wikipedia.org/wiki/European_Union, 2020-05-05
import pandas as pd
from datetime import datetime
from app.country.model import Country, EU

eu = [
    {
        'valid_from': datetime.strptime('01-01-2015', '%d-%m-%Y').date(),
        'valid_to': datetime.strptime('31-12-2020', '%d-%m-%Y').date()
    }
]



class EUSeedService:
    @staticmethod
    def append_countries_to_eu():
        file = '/Users/tm/Projects/NTAMAZON/webapp/api/commands/eu.csv'
        df = pd.read_csv(file)
        eu = EU.query.filter_by(id=1).first()
        eu_size = 0

        for row in range(len(df.index)):
            if bool(df.iloc[row]['eu_1']):
                country = Country.query.filter_by(code=df.iloc[row]['code']).first()
                eu.append(country)
                eu_size +=1

        response_object = {
            'status': 'success',
            'message': 'EU comprises {} countries.'.format(eu_size)
        }
        return response_object
