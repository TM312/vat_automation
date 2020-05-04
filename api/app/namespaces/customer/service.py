from !!!! import VATINService


class CustomerService:

    @staticmethod
    def get_customer_type(check_required: bool, country_code: str, number: str, date: date) -> str:
        if not number:
            customer_type = 'B2C'

        elif number and check_required:
            customer_type = 'B2B' if VATINService.check_validity(
                country_code, number, date) else 'B2C'

        elif number and not check_required:
            customer_type = 'B2B'

        return customer_type
