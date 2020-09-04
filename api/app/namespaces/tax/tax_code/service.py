from typing import List
from app.extensions import db


from . import TaxCode
from .interface import TaxCodeInterface
from ...transaction_input import TransactionInput
from ...utils.service import NotificationService


class TaxCodeService:
    @staticmethod
    def get_all() -> List[TaxCode]:
        tax_codes = TaxCode.query.all()
        return tax_codes

    @staticmethod
    def get_by_code(code: str) -> TaxCode:
        return TaxCode.query.filter(TaxCode.code == code).first()

    @staticmethod
    def update(code: str, data_changes: TaxCodeInterface) -> TaxCode:
        tax_code = TaxCodeService.get_by_code(code)
        tax_code.update(data_changes)
        db.session.commit()
        return tax_code

    @staticmethod
    def delete_by_code(code: str):
        tax_code = TaxCode.query.filter(TaxCode.code == code).first()
        if tax_code:
            db.session.delete(tax_code)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'TaxCode (code: {}) has been successfully deleted.'.format(code)
            }
            return response_object
        else:
            raise NotFound('This tax_code does not exist.')

    @staticmethod
    def create(tax_code_data: TaxCodeInterface) -> TaxCode:

        new_tax_code = TaxCode(
            code=tax_code_data.get('code'),
            description=tax_code_data.get('description')
        )

        #add seller firm to db
        db.session.add(new_tax_code)
        db.session.commit()

        return new_tax_code




    @staticmethod
    def compare_calculation_reference(transaction_id: int, transaction_input: TransactionInput, tax_code_code: str, calculated_tax_code_code) -> None:
        if calculated_tax_code_code != tax_code_code:
            notification_data=NotificationService.create_transaction_notification_data(
                main_subject='Item Tax Code',
                original_filename=transaction_input.original_filename,
                status='warning',
                reference_value=tax_code_code,
                calculated_value=calculated_tax_code_code,
                transaction_id=transaction_id
            )
            try:
                NotificationService.create_transaction_notification(notification_data)
            except:
                db.session.rollback()
                raise
