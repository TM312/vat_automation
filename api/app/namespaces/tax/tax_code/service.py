from typing import List
from app.extensions import db


from . import TaxCode
from .interface import TaxCodeInterface


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
