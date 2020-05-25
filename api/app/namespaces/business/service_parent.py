from typing import Union
from .model_parent import Business
from .accounting_firm.model import AccountingFirm
from .seller_firm.model import SellerFirm
from werkzeug.exceptions import NotFound

class BusinessService:

    @staticmethod
    def get_by_name_address_or_None(name: str, address: str) -> Union[AccountingFirm, SellerFirm]:
        business = BusinessService.get_by_name_or_None(name)
        if isinstance(business, None):
            business = BusinessService.get_by_address_or_None(address)
        return business


    @staticmethod
    def get_by_name_or_None(name: str) -> Union[AccountingFirm, SellerFirm]:
        return Business.query.filter_by(name=name).first()

    @staticmethod
    def get_by_address_or_None(address: str) -> Union[AccountingFirm, SellerFirm]:
        return Business.query.filter_by(address=address).first()
