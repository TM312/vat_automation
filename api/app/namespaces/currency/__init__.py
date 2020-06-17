from .model import Currency
from .schema import currency_dto


BASE_ROUTE = "currency"

def attach_currency(api, app):
    from .controller import ns as currency_ns
    api.add_namespace(currency_ns, path=f"/{BASE_ROUTE}")
