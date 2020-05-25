from .model import Customer
from .interface import CustomerInterface
from ..tax.vatin.model import VATIN
from ..tax.vatin.service import VATINService, VIESService
from ..transaction_input.model import TransactionInput
from ..business.service_parent import BusinessService

from datetime import date

class CustomerService:

    @staticmethod
    def get_customer(name: str, address: str) -> Customer:
        return Customer.query.filter(name=name, address=address).first()


    @staticmethod
    def create_customer(customer_data: CustomerInterface) -> Customer:
        new_customer = Customer(
            name=customer_data.get('name'),
            address=customer_data.get('address')
        )

        db.session.add(new_customer)
        db.session.commit()

        return new_customer


    @staticmethod
    def get_customer_or_None(customer_vatin, customer_relationship):
        if customer_vatin.valid and customer_relationship == 'B2B':
            try:
                customer = CustomerService.get_or_create_customer(customer_vatin)
                return customer
            except:
                db.session.rollback()
                raise
        else:
            return None


    @staticmethod
    def get_customer_relationship(customer_vatin: VATIN, check_required: bool) -> str:

        if isinstance(customer_vatin, VATIN):
            bool_as_code = 'B2B' if customer_vatin.valid else 'B2C'
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
                customer_vatin = VATINService.get_vatin_if_number(country_code_temp, number_temp, date)
                business = BusinessService.get_by_name_address_or_None(customer_vatin.name, customer_vatin.address)

                if not isinstance(business, None):
                    data_changes = {'business_id': business.id}
                    customer_vatin.update(data_changes)
                    db.session.commit()

            except:
                raise

            return customer_vatin





    @staticmethod
    def get_or_create_customer(customer_vatin: VATIN) -> Customer:
        name = VIESService.sanitize_response_detail(customer_vatin, parameter='name')
        address = VIESService.sanitize_response_detail(customer_vatin, parameter='address')

        customer_data = {
            'name': name,
            'address': address
        }

        customer = CustomerService.get_customer(name,address)
        if isinstance(customer, Customer) and (name != customer.name or address != customer.address):
            customer.update(customer_data)
            db.session.commit()

        else:
            new_customer = CustomerService.create_customer(customer_data)
            customer = new_customer

        return customer


    @staticmethod
    def compare_calculation_reference(transaction_input: TransactionInput, customer_vatin: VATIN):
        if transaction_input.customer_name and customer_vatin.name and transaction_input.customer_name != customer_vatin.name:
            notification_data = NotificationService.create_notification_data(main_subject='Customer Name', original_filename=transaction_input.original_filename, status='info', reference_value=transaction_input.customer_name, calculated_value=item.name, transaction_input_id=customer_vatin.name)
            NotificationService.create_transaction_notification(notification_data)
