from .model import TaxRecord
from .schema import tax_record_dto, tax_record_dto_admin

BASE_ROUTE = "tax_record"


def attach_tax_record(api, app):
    from .controller import ns as tax_record_ns
    api.add_namespace(tax_record_ns, path=f"/{BASE_ROUTE}")
