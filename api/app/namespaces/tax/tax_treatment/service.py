from typing import List
from app.extensions import db


from . import TaxTreatment
from .interface import TaxTreatmentInterface



class TaxTreatmentService:
    @staticmethod
    def get_all() -> List[TaxTreatment]:
        tax_treatments = TaxTreatment.query.all()
        return tax_treatments

    @staticmethod
    def get_by_code(code: str) -> TaxTreatment:
        return TaxTreatment.query.filter(TaxTreatment.code == code).first()

    @staticmethod
    def update(code: str, data_changes: TaxTreatmentInterface) -> TaxTreatment:
        tax_treatment = TaxTreatmentService.get_by_code(code)
        tax_treatment.update(data_changes)
        db.session.commit()
        return tax_treatment

    @staticmethod
    def delete_by_code(code: str):
        tax_treatment = TaxTreatment.query.filter(TaxTreatment.code == code).first()
        if tax_treatment:
            db.session.delete(tax_treatment)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'TaxTreatment (code: {}) has been successfully deleted.'.format(code)
            }
            return response_object
        else:
            raise NotFound('This tax_treatment does not exist.')

    @staticmethod
    def create(tax_treatment_data: TaxTreatmentInterface) -> TaxTreatment:

        new_tax_treatment = TaxTreatment(
            code=tax_treatment_data.get('code'),
            name=tax_treatment_data.get('name'),
            description=tax_treatment_data.get('name')
        )

        #add seller firm to db
        db.session.add(new_tax_treatment)
        db.session.commit()

        return new_tax_treatment
