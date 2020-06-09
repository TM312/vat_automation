from ..interface_parent import BusinessInterface
from typing import List

class CustomerFirmInterface(BusinessInterface):
    transactions: List['app.namespaces.transaction.Transaction']
