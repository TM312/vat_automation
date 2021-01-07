from typing import List
from ..interface_parent import BusinessInterface

class SellerFirmInterface(BusinessInterface):
    claimed: bool
    establishment_country_code: str
    user_public_id: str
