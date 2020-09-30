from datetime import date
from typing import List, Dict

from app.extensions import db
from . import CustomerFirm
from .interface import CustomerFirmInterface

from .. import Business
from ..service_parent import BusinessService
from ...utils.service import NotificationService

from ...tax.vatin import VATIN
from ...tax.vatin.service import VATINService, VIESService


class CustomerFirmService:
    @staticmethod
    def get_all() -> List[CustomerFirm]:
        seller_firms = CustomerFirm.query.all()
        return seller_firms

    @staticmethod
    def get_by_id(seller_firm_id: int) -> CustomerFirm:
        return CustomerFirm.query.filter_by(id=seller_firm_id).first()


    @staticmethod
    def update(seller_firm_id: int, data_changes: CustomerFirmInterface) -> CustomerFirm:
        seller_firm = CustomerFirmService.get_by_id(seller_firm_id)
        seller_firm.update(data_changes)
        db.session.commit()
        return seller_firm

    @staticmethod
    def delete_by_id(seller_firm_id: int) -> Dict:
        #check if accounting business exists in db
        seller_firm = CustomerFirm.query.filter_by(id = seller_firm_id).first()
        if seller_firm:
            db.session.delete(seller_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller firm (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')


    @staticmethod
    def create(customer_firm_data: CustomerFirmInterface) -> CustomerFirm:
        new_customer_firm= CustomerFirm(
            name=customer_firm_data.get('name'),
            address=customer_firm_data.get('address')
        )

        db.session.add(new_customer_firm)
        db.session.commit()

        return new_customer_firm


    @staticmethod
    def get_customer_firm_or_None(customer_firm_vatin, customer_relationship):
        if isinstance(customer_firm_vatin, VATIN) and customer_firm_vatin.valid and customer_relationship == 'B2B':
            try:
                customer_firm = CustomerFirmService.get_or_create_customer_firm(customer_firm_vatin)
            except:
                db.session.rollback()
                raise

            return customer_firm


    @staticmethod
    def get_customer_relationship(transaction_type_code: str, customer_firm_vatin: VATIN, check_required: bool) -> str:
        customer_relationship_checked = False

        if transaction_type_code == 'MOVEMENT':
            customer_relationship = 'B2B'

        elif isinstance(customer_firm_vatin, VATIN):
            bool_as_code = 'B2B' if customer_firm_vatin.valid else 'B2C'
            customer_relationship_checked = True
            customer_relationship = 'B2B' if not check_required else bool_as_code

            # Create Notification if bool_as_code != customer_relationship !!!!


        else:
            customer_relationship = 'B2C'

        return customer_relationship, customer_relationship_checked





    @staticmethod
    def get_or_create_customer_firm(customer_firm_vatin: VATIN) -> CustomerFirm:
        name = customer_firm_vatin.name if not customer_firm_vatin.name == '---' else None
        address = customer_firm_vatin.address if not customer_firm_vatin.address == '---' else None

        customer_firm = BusinessService.get_by_name_address_or_None(name, address)

        customer_firm_data = {
            'name': name,
            'address': address
        }

        if isinstance(name, str) and isinstance(address, str):
            if isinstance(customer_firm, Business):
                if name != customer_firm.name or address != customer_firm.address:
                    customer_firm.update(customer_firm_data)
                    db.session.commit()

            else:
                try:
                    new_customer_firm = CustomerFirmService.create(customer_firm_data)
                except:
                    db.session.rollback()
                    raise

                    customer_firm = new_customer_firm

            if not customer_firm.vat_numbers or customer_firm_vatin not in customer_firm.vat_numbers:
                try:
                    customer_firm.vat_numbers.append(customer_firm_vatin)
                    db.session.commit()
                except:
                    db.session.rollback()

        return customer_firm


    @staticmethod
    def compare_calculation_reference(transaction_id: int, transaction_input: 'app.namespaces.transaction_input.TransactionInput', customer_firm_vatin: VATIN):
        if transaction_input.customer_firm_name and customer_firm_vatin.name and transaction_input.customer_firm_name != customer_firm_vatin.name:
            notification_data = NotificationService.create_transaction_notification_data(main_subject='Customer Firm Name', original_filename=transaction_input.original_filename, status='info', reference_value=transaction_input.customer_firm_name, calculated_value=customer_firm_vatin.name, transaction_id=transaction_id)
            NotificationService.create_transaction_notification(notification_data)
