from .model import ExchangeRateCollection, ExchangeRatesEUR, ExchangeRatesGBP, ExchangeRatesCZK, ExchangeRatesPLN #noqa
from werkzeug.exceptions import InternalServerError

from datetime import datetime

class ExchangeRatesService:

    @staticmethod
    def retrieve_ecb_exchange_rates():
        #df = pd.read_csv(filepath, sep=',')
        exchange_rate_dict = {}

        #get exchange rate data
        import requests
        r = requests.get(
            'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml', stream=True)
        from xml.etree import ElementTree as ET
        tree = ET.parse(r.raw)
        root = tree.getroot()
        namespaces = {
            'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):
            # data is added to dict
            exchange_rate_dict[str(cube.attrib['currency'])] = cube.attrib['rate']
        #daily_rate_dict['Date'] = datetime.date.today().strftime("%d.%m.%y")
        return exchange_rate_dict


    def create_exchange_rate_collection(date) -> ExchangeRateCollection:
        exchange_rate_collection = ExchangeRateCollection.query.filter_by(date=date).first()

        if not exchange_rate_collection:
            #create new exchange_rate_collection based on TaxAuditor model
            new_exchange_rate_collection = ExchangeRateCollection(
                date=date,
                created_on=datetime.utcnow()
            )

            #add exchange_rate_collection to db
            db.session.add(new_exchange_rate_collection)
            db.session.commit()

            return new_exchange_rate_collection


    def create_exchange_rates_EUR(date) -> ExchangeRatesEUR:
        exchange_rate_collection = ExchangeRateCollection.query.filter_by(
            date=date).first()

        if exchange_rate_collection:

            #api call to ECB
            exchange_rate_dict = ExchangeRatesService.retrieve_ecb_exchange_rates()

            new_exchange_rates_EUR = ExchangeRatesEUR(
                source='ECB',
                created_on=datetime.utcnow(),
                date=exchange_rate_collection.date,
                exchange_rate_collection_id=exchange_rate_collection.id,
                eur=1.0000,
                gbp=exchange_rate_dict['GBP'],
                czk=exchange_rate_dict['CZK'],
                pln=exchange_rate_dict['PLN']
            )

            #add exchange_rate_collection to db
            db.session.add(new_exchange_rates_EUR)
            db.session.commit()

            return new_exchange_rates_EUR

        else:
            response_object = {
                'status' : 'error',
                'message': 'The corresponding exchange rate collection can not be found.'
            }
            raise InternalServerError(response_object)


    def create_exchange_rates_GBP(date) -> ExchangeRatesGBP:
        exchange_rate_collection = ExchangeRateCollection.query.filter_by(
                date=date).first()

        exchange_rates_EUR = ExchangeRatesEUR.query.filter_by(
                exchange_rate_collection_id=exchange_rate_collection.id).first()

        if exchange_rate_collection and exchange_rates_EUR:
            gbp_eur = 1/exchange_rates_EUR.gbp

            new_exchange_rates_GBP = ExchangeRatesEUR(
                source='ECB',
                created_on=datetime.utcnow(),
                date=exchange_rate_collection.date,
                exchange_rate_collection_id=exchange_rate_collection.id,
                eur=gbp_eur,
                gbp=1.0000,
                czk=gbp_eur * exchange_rates_EUR.czk,
                pln=gbp_eur * exchange_rates_EUR.pln
            )

            #add exchange_rate_collection to db
            db.session.add(new_exchange_rates_GBP)
            db.session.commit()

            return new_exchange_rates_GBP

        else:
            response_object = {
                'status': 'error',
                'message': 'An error occured.'
            }
            raise InternalServerError(response_object)


    def create_exchange_rates_CZK(date) -> ExchangeRatesCZK:
        exchange_rate_collection = ExchangeRateCollection.query.filter_by(
            date=date).first()

        exchange_rates_EUR = ExchangeRatesEUR.query.filter_by(
            exchange_rate_collection_id=exchange_rate_collection.id).first()

        if exchange_rate_collection and exchange_rates_EUR:
            czk_eur = 1/exchange_rates_EUR.czk
            new_exchange_rates_CZK = ExchangeRatesEUR(
                source='ECB',
                created_on=datetime.utcnow(),
                date=exchange_rate_collection.date,
                exchange_rate_collection_id=exchange_rate_collection.id,
                eur=czk_eur,
                gbp=czk_eur * exchange_rates_EUR.gbp,
                czk=1.0000,
                pln=czk_eur * exchange_rates_EUR.pln
            )

            #add exchange_rate_collection to db
            db.session.add(new_exchange_rates_CZK)
            db.session.commit()

            return new_exchange_rates_CZK

        else:
            response_object = {
                'status': 'error',
                'message': 'An error occured.'
            }
            raise InternalServerError(response_object)

    def create_exchange_rates_PLN(date) -> ExchangeRatesPLN:
        exchange_rate_collection = ExchangeRateCollection.query.filter_by(
            date=date).first()

        exchange_rates_EUR = ExchangeRatesEUR.query.filter_by(
            exchange_rate_collection_id=exchange_rate_collection.id).first()

        if exchange_rate_collection and exchange_rates_EUR:
            pln_eur = 1/exchange_rates_EUR.pln
            new_exchange_rates_PLN = ExchangeRatesEUR(
                source='ECB',
                created_on=datetime.utcnow(),
                date=exchange_rate_collection.date,
                exchange_rate_collection_id=exchange_rate_collection.id,
                eur=pln_eur,
                gbp=pln_eur * exchange_rates_EUR.gbp,
                czk=pln_eur * exchange_rates_EUR.czk,
                pln=1.0000
            )

            #add exchange_rate_collection to db
            db.session.add(new_exchange_rates_PLN)
            db.session.commit()

            return new_exchange_rates_PLN

        else:
            response_object = {
                'status': 'error',
                'message': 'An error occured.'
            }
            raise InternalServerError(response_object)
