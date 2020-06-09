from .model import ExchangeRate
from .schema import exchange_rate_dto


BASE_ROUTE = "exchange_rate"


def attach_exchange_rate(api, app):
    from .controller import ns as exchange_rate_ns
    api.add_namespace(exchange_rate_ns, path=f"/{BASE_ROUTE}")
