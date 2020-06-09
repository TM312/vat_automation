from typing import Union, List
from . import Business, AccountingFirm, SellerFirm, CustomerFirm

class BusinessService:

    @staticmethod
    def get_by_name_address_or_None(name: str, address: str) -> Union[AccountingFirm, SellerFirm, CustomerFirm]:
        business = BusinessService.get_by_name_or_None(name)
        if isinstance(business, None):
            business = BusinessService.get_by_address_or_None(address)
        return business


    @staticmethod
    def get_by_name_or_None(name: str) -> Union[AccountingFirm, SellerFirm, CustomerFirm]:
        return Business.query.filter_by(name=name).first()

    @staticmethod
    def get_by_address_or_None(address: str) -> Union[AccountingFirm, SellerFirm, CustomerFirm]:
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
        business = Business.query.filter(Business.business_id == business_id).first()
        if not business:
            return []
        db.session.delete(business)
        db.session.commit()
        return [business_id]
