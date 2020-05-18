from ..interface_parent import BusinessInterface

class SellerFirmInterface(BusinessInterface):
    claimed: bool
    establishment_country_code: str
    accounting_firm_id: int
    accounting_firm_client_id: str
