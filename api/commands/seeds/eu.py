#source: https: // en.wikipedia.org/wiki/European_Union, 2020-05-05
import pandas as pd
from datetime import datetime
from os import path

from app.namespaces.country.model import Country, EU


class EUSeedService:

    @staticmethod
    def seed_eu():
        from . import SERVICE_START_DATE

        eu = [
            {
                'valid_from': SERVICE_START_DATE,
                'valid_to': datetime.strptime('31-12-2020', '%d-%m-%Y').date()
            }
        ]
        return eu


    @staticmethod
    def append_countries_to_eu():
        from . import BASE_PATH_SEEDS

        file = 'eu.csv'
        dirpath = path.join(
            BASE_PATH_SEEDS,
            file)

        df = pd.read_csv(dirpath)
        eu = EU.query.first()
        eu_size = 0

        try:
            for row in range(len(df.index)):
                if bool(df.iloc[row]['eu_1']):
                    country = Country.query.filter_by(code=df.iloc[row]['code']).first()
                    print('appending {} to eu'.format(str(country.code)))
                    eu.countries.append(country)
                    eu_size +=1

            response_object = {
                'status': 'success',
                'message': 'EU comprises {} countries.'.format(eu_size)
            }

        except:
            response_object = {
                'status': 'error',
                'message': 'Failed attach countries to EU.'
            }

        return response_object
