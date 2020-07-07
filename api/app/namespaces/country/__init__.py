from .model import Country, EU
from .schema import country_dto, country_sub_dto, eu_dto


BASE_ROUTE = "country"

def attach_country(api, app):
    from .controller import ns as country_ns
    api.add_namespace(country_ns, path=f"/{BASE_ROUTE}")
