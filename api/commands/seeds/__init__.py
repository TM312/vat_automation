from datetime import datetime

#BASE_PATH_SEEDS = '/var/lib/seeds/'
BASE_PATH_SEEDS = '/home/data/seeds'


SERVICE_START_DATE = datetime.strptime('01-06-2018', '%d-%m-%Y').date()
TAX_DEFAULT_VALIDITY = datetime.strptime('31-12-2099', '%d-%m-%Y').date()
