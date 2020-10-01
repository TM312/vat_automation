from typing import Union, List
from . import Business
from .accounting_firm import AccountingFirm
from .seller_firm import SellerFirm

from .interface_parent import BusinessInterface


class BusinessService:

    @staticmethod
    def get_by_name_address_or_None(name: str, address: str) -> Union[AccountingFirm, SellerFirm]:
        business = BusinessService.get_by_name_or_None(name)
        if not isinstance(business, Business):
            business = BusinessService.get_by_address_or_None(address)

        return business


    @staticmethod
    def get_by_name_or_None(name: str) -> Union[AccountingFirm, SellerFirm]:
        return Business.query.filter_by(name=name).first()

    @staticmethod
    def get_by_address_or_None(address: str) -> Union[AccountingFirm, SellerFirm]:
        return Business.query.filter_by(address=address).first()

    @staticmethod
    def get_all() -> List[Business]:
        return Business.query.all()

    @staticmethod
    def get_by_id(business_id: int) -> Business:
        return Business.query.get(business_id)

    @staticmethod
    def update(business: Business, data_changes: BusinessInterface) -> Business:
        business.update(data_changes)
        db.session.commit()
        return business

    @staticmethod
    def delete_by_id(business_id: int) -> List[int]:
        business = BusinessService.get_by_id(business_id)
        if not business:
            return []
        db.session.delete(business)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return [business_id]
