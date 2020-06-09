from mypy_extensions import TypedDict
from typing import List
from ..interface_parent import BusinessInterface

class AccountingFirmInterface(BusinessInterface):
    employees: List['app.namespaces.users.tax_auditor.TaxAuditor']
    clients: List['app.namespaces.business.seller_firm.SellerFirm']
