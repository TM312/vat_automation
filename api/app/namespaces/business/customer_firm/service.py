from datetime import date

from .model import CustomerFirm
from .interface import CustomerFirmInterface

from ...tax.vatin.model import VATIN
from ...tax.vatin.service import VATINService, VIESService
from ...transaction_input.model import TransactionInput
from ...business.service_parent import BusinessService


class CustomerFirmService:

    @staticmethod
    def get_customer_firm(name: str, address: str) -> Customer:
        return CustomerFirm.query.filter(name=name, address=address).first()


    @staticmethod
    def create_customer_firm(customer_firm_data: CustomerFirmInterface) -> Customer:
        new_customer_firm= CustomerFirm(
            name=customer_firm_data.get('name'),
            address=customer_firm_data.get('address'),
            vatin_id = customer_firm_data.get('vatin_id')
        )

        db.session.add(new_customer)
        db.session.commit()

        return new_customer


    @staticmethod
    def get_customer_firm_or_None(customer_firm_vatin, customer_relationship):
        if customer_firm_vatin.valid and customer_relationship == 'B2B':
            try:
                customer_firm= CustomerFirmService.get_or_create_customer_firm(customer_firm_vatin)
                return customer
            except:
                db.session.rollback()
                raise
        else:
            return None


    @staticmethod
    def get_customer_relationship(customer_firm_vatin: VATIN, check_required: bool) -> str:

        if isinstance(customer_firm_vatin, VATIN):
            bool_as_code = 'B2B' if customer_firm_vatin.valid else 'B2C'
            customer_relationship = 'B2B' if not check_required else bool_as_code
            # Create Notification if bool_as_code != customer_relationship !!!!


        else:
            customer_relationship = 'B2C'

        return customer_relationship


    @staticmethod
    def get_vatin_or_None(customer_vat_check_required: bool, country_code_temp: str, number_temp: str, date: date) -> VATIN:
        if not customer_vat_check_required:
            return None
        else:
            try:
                customer_firm_vatin = VATINService.get_vatin_if_number(country_code_temp, number_temp, date)
                business = BusinessService.get_by_name_address_or_None(customer_firm_vatin.name, customer_firm_vatin.address)

                if not isinstance(business, None):
                    data_changes = {'business_id': business.id}
                    customer_firm_vatin.update(data_changes)
                    db.session.commit()

            except:
                raise

            return customer_firm_vatin





    @staticmethod
    def get_or_create_customer_firm(customer_firm_vatin: VATIN) -> Customer:
        name = VIESService.sanitize_response_detail(customer_firm_vatin, parameter='name')
        address = VIESService.sanitize_response_detail(customer_firm_vatin, parameter='address')

        customer_firm= CustomerFirmService.get_customer_firm(name, address)

        customer_firm_data = {
            'name': name,
            'address': address,
            'vatin_id': customer_firm_vatin.id
        }

        if isinstance(customer, Customer) and (name != customer_firm.name or address != customer_firm.address):
            customer_firm.update(customer_firm_data)
            db.session.commit()

        else:
            new_customer_firm= CustomerFirmService.create_customer_firm(customer_firm_data)
            customer_firm= new_customer

        return customer


    @staticmethod
    def compare_calculation_reference(transaction_input: TransactionInput, customer_firm_vatin: VATIN):
        if transaction_input.customer_firm_name and customer_firm_vatin.name and transaction_input.customer_firm_name != customer_firm_vatin.name:
            notification_data = NotificationService.create_notification_data(main_subject='Customer Firm Name', original_filename=transaction_input.original_filename, status='info', reference_value=transaction_input.customer_firm_name, calculated_value=customer_firm_vatin.name, transaction_input_id=transaction_input.id)
            NotificationService.create_transaction_notification(notification_data)
