from .accounting_firm.interface import AccountingFirmInterface
from .accounting_firm.schema import accounting_firm_dto
from .accounting_firm.service import AccountingFirmService
from .accounting_firm.model import AccountingFirm

from .seller_firm.interface import SellerFirmInterface
from .seller_firm.schema import seller_firm_dto
from .seller_firm.service import SellerFirmService
from .seller_firm.model import SellerFirm



BASE_ROUTE = "business"


def attach_business(api, app):
    from .seller_firm.controller import ns as seller_firm_ns
    from .accounting_firm.controller import ns as accounting_firm_ns
    from .controller_parent import ns as business_ns

    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/seller_firm")
    api.add_namespace(accounting_firm_ns, path=f"/{BASE_ROUTE}/accounting_firm")
    api.add_namespace(user_ns, path=f"/{BASE_ROUTE}")
