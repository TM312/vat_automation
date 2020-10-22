from datetime import date
from typing import List, Dict

from werkzeug.exceptions import NotFound
from app.extensions import db


from . import VatThreshold
from .interface import VatThresholdInterface



class VatThresholdService:
    @staticmethod
    def get_all() -> List[VatThreshold]:
        return VatThreshold.query.all()

    @staticmethod
    def get_by_id(vat_threshold_id: int) -> VatThreshold:
        return VatThreshold.query.filter_by(id=vat_threshold_id).first()


    @staticmethod
    def update(vat_threshold_id: int, data_changes: VatThresholdInterface) -> VatThreshold:
        vat_threshold = VatThresholdService.get_by_id(vat_threshold_id)
        vat_threshold.update(data_changes)
        db.session.commit()
        return vat_threshold

    @staticmethod
    def delete_by_id(vat_threshold_id: int) -> Dict:
        vat_threshold = VatThresholdService.get_by_id(vat_threshold_id)
        if vat_threshold:
            db.session.delete(vat_threshold)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Vat Threshold (id: {}) has been successfully deleted.'.format(vat_threshold_id)
            }
            return response_object
        else:
            raise NotFound('This vat threshold does not exist.')

    @staticmethod
    def create(vat_threshold_data: VatThresholdInterface) -> VatThreshold:

        new_vat_threshold = VatThreshold(
            valid_from = vat_threshold_data.get('valid_from'),
            valid_to = vat_threshold_data.get('valid_to'),
            country_code = vat_threshold_data.get('country_code'),
            tax_code_code = vat_threshold_data.get('tax_code_code'),
            tax_rate_type_code = vat_threshold_data.get('tax_rate_type_code'),
            rate = vat_threshold_data.get('rate')
        )

        #add seller firm to db
        db.session.add(new_vat_threshold)
        db.session.commit()

        return new_vat_threshold
