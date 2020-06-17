from typing import List
from ..interface_parent import BusinessInterface

class SellerFirmInterface(BusinessInterface):
    claimed: bool
    establishment_country_code: str
    employees: List['app.namespaces.business.seller.Seller']
    distance_sales: List['app.namespaces.distance_sale.DistanceSale']
    items: List['app.namespaces.item.interface.ItemInterface']

    accounting_firm_id: int
    accounting_firm_client_id: str
    accounts: List['app.namespaces.account.Account']
    tax_records: List['app.namespaces.tax_record.TaxRecord']
