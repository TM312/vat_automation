from datetime import date
from typing import List, Dict

from . import CustomerFirm
from .interface import CustomerFirmInterface

from .. import Business
from ..service_parent import BusinessService

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
    def get_by_name_address(name: str, address: str) -> CustomerFirm:
        return CustomerFirm.query.filter(name=name, address=address).first()


    @staticmethod
    def create(customer_firm_data: CustomerFirmInterface) -> CustomerFirm:
        new_customer_firm= CustomerFirm(
            name=customer_firm_data.get('name'),
            address=customer_firm_data.get('address')
        )

        db.session.add(new_customer)
        db.session.commit()

        return new_customer


    @staticmethod
    def get_customer_firm_or_None(customer_firm_vatin, customer_relationship):
        if isinstance(customer_firm_vatin, VATIN) and customer_firm_vatin.valid and customer_relationship == 'B2B':
            try:
                customer_firm= CustomerFirmService.get_or_create_customer_firm(customer_firm_vatin)
                return customer
            except:
                db.session.rollback()
                raise

    @staticmethod
    def get_customer_relationship(customer_firm_vatin: VATIN, check_required: bool) -> str:
        customer_relationship_checked = False

        if isinstance(customer_firm_vatin, VATIN):
            bool_as_code = 'B2B' if customer_firm_vatin.valid else 'B2C'
            customer_relationship_checked = True
            customer_relationship = 'B2B' if not check_required else bool_as_code

            # Create Notification if bool_as_code != customer_relationship !!!!


        else:
            customer_relationship = 'B2C'

        return customer_relationship, customer_relationship_checked


    @staticmethod
    def get_vatin_or_None(customer_vat_check_required: bool, country_code_temp: str, number_temp: str, date: date) -> VATIN:
        print('customer_vat_check_required: ', customer_vat_check_required, flush=True)
        if not customer_vat_check_required:
            return None
        else:
            try:
                customer_firm_vatin = VATINService.get_vatin_if_number(country_code_temp, number_temp, date)
                if isinstance(customer_firm_vatin, VATIN):
                    business = BusinessService.get_by_name_address_or_None(customer_firm_vatin.name, customer_firm_vatin.address)

                    if isinstance(business, Business):
                        data_changes = {'business_id': business.id}
                        customer_firm_vatin.update(data_changes)
                        db.session.commit()

                    return customer_firm_vatin

                else:
                    return None


            except:
                raise






    @staticmethod
    def get_or_create_customer_firm(customer_firm_vatin: VATIN) -> CustomerFirm:
        name = VIESService.sanitize_response_detail(customer_firm_vatin, parameter='name')
        address = VIESService.sanitize_response_detail(customer_firm_vatin, parameter='address')

        customer_firm= CustomerFirmService.get_by_name_address(name, address)

        customer_firm_data = {
            'name': name,
            'address': address
        }

        if not (isinstance(name, None) or isinstance(address, None)):
            if isinstance(customer, Customer) and (name != customer_firm.name or address != customer_firm.address):
                customer_firm.update(customer_firm_data)
                db.session.commit()

            else:
                new_customer_firm= CustomerFirmService.create(customer_firm_data)
                customer_firm = new_customer_firm

            if customer_firm_vatin not in customer_firm.vat_numbers:
                customer_firm.vat_numbers.append(customer_firm_vatin)
                db.session.commit()

        return customer_firm


    @staticmethod
    def compare_calculation_reference(transaction_input: 'app.namespaces.transaction_input.TransactionInput', customer_firm_vatin: VATIN):
        if transaction_input.customer_firm_name and customer_firm_vatin.name and transaction_input.customer_firm_name != customer_firm_vatin.name:
            notification_data = NotificationService.create_notification_data(main_subject='Customer Firm Name', original_filename=transaction_input.original_filename, status='info', reference_value=transaction_input.customer_firm_name, calculated_value=customer_firm_vatin.name, transaction_input_id=transaction_input.id)
            NotificationService.create_transaction_notification(notification_data)
