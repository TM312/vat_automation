from typing import List
from app.extensions import db


from . import TaxRateType
from .interface import TaxRateTypeInterface


class TaxRateTypeService:
    @staticmethod
    def get_all() -> List[TaxRateType]:
        tax_rate_types = TaxRateType.query.all()
        return tax_rate_types

    @staticmethod
    def get_by_code(tax_rate_type_code: str) -> TaxRateType:
        return TaxRateType.query.filter_by(code = tax_rate_type_code).first()

    @staticmethod
    def update(tax_rate_type_code: str, data_changes: TaxRateTypeInterface) -> TaxRateType:
        tax_rate_type = TaxRateTypeService.get_by_code(tax_rate_type_code)
        tax_rate_type.update(data_changes)
        db.session.commit()
        return tax_rate_type

    @staticmethod
    def delete_by_code(tax_rate_type_code: str):
        tax_rate_type = TaxRateTypeService.get_by_code(tax_rate_type_code)
        if tax_rate_type:
            db.session.delete(tax_rate_type)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'TaxRateType (code: {}) has been successfully deleted.'.format(tax_rate_type_code)
            }
            return response_object
        else:
            raise NotFound('This tax_rate_type does not exist.')

    @staticmethod
    def create(tax_rate_type_data: TaxRateTypeInterface) -> TaxRateType:

        new_tax_rate_type = TaxRateType(
            code=tax_rate_type_data.get('code'),
            description=tax_rate_type_data.get('description')
        )

        #add seller firm to db
        db.session.add(new_tax_rate_type)
        db.session.commit()

        return new_tax_rate_type
