from ..tax import VATINService

class CustomerService:

    @staticmethod
    def get_customer_relationship(check_required: bool, country_code: str, number: str, date: date) -> str:
        if not number:
            customer_relationship = 'B2C'

        elif number and check_required:
            customer_relationship = 'B2B' if VATINService.check_validity(country_code, number, initial_tax_date=date) else 'B2C'

        elif number and not check_required:
            customer_relationship = 'B2B'

        return customer_relationship
