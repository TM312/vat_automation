from datetime import date
from typing import List, Dict

from werkzeug.exceptions import NotFound
from app.extensions import db


from . import VatThreshold, VatThresholdHistory
from .interface import VatThresholdInterface



class VatThresholdService:
    @staticmethod
    def get_all() -> List[VatThreshold]:
        return VatThreshold.query.all()

    @staticmethod
    def get_by_id(vat_threshold_id: int) -> VatThreshold:
        return VatThreshold.query.filter_by(id=vat_threshold_id).first()

    @staticmethod
    def get_by_public_id(vat_threshold_public_id: str) -> VatThreshold:
        return VatThreshold.query.filter_by(public_id=vat_threshold_public_id).first()


    @staticmethod
    def update(vat_threshold_id: int, data_changes: VatThresholdInterface) -> VatThreshold:
        vat_threshold = VatThresholdService.get_by_id(vat_threshold_id)
        if isinstance(vat_threshold, VatThreshold):
            vat_threshold.update(data_changes)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

        return vat_threshold

    @staticmethod
    def update_by_public_id(vat_threshold_public_id: str, data_changes: VatThresholdInterface) -> VatThreshold:
        vat_threshold = VatThresholdService.get_by_public_id(vat_threshold_public_id)
        if isinstance(vat_threshold, VatThreshold):
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
    def delete_by_public_id(vat_threshold_public_id: str) -> Dict:
        vat_threshold = VatThresholdService.get_by_public_id(vat_threshold_public_id)
        if vat_threshold:
            db.session.delete(vat_threshold)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Vat Threshold (id: {}) has been successfully deleted.'.format(vat_threshold_public_id)
            }
            return response_object
        else:
            raise NotFound('This vat_threshold does not exist.')

    @staticmethod
    def create(vat_threshold_data: VatThresholdInterface) -> VatThreshold:

        new_vat_threshold = VatThreshold(
            created_by = vat_threshold_data.get('created_by'),
            country_code = vat_threshold_data.get('country_code'),
            value = vat_threshold_data.get('value'),
            currency_code = vat_threshold_data.get('currency_code')
        )

        #add seller firm to db
        db.session.add(new_vat_threshold)
        db.session.commit()

        vat_threshold_data['vat_threshold_id'] = new_vat_threshold.id
        try:
            VatThresholdHistoryService.create(vat_threshold_data)
        except:
            db.session.rollback()
            raise

        return new_vat_threshold



class VatThresholdHistoryService:

    @staticmethod
    def handle_update(vat_threshold_id, data_changes):

        """
        When updating 3 cases can exist:

        CASE EARLIER: The update's valid_from attribute is EARLIER than any other vat threshold history object.
            1. New vat threshold history is created
            2. Oldest vat threshold history retrieved
            3. Missing data change attributes complemented by those from oldest vat threshold history
            4. New vat threshold history valid_to == oldest vat threshold history valid_from - timedelta(days=1)

        CASE EQUAL: The update's valid_from attribute is EQUAL to another vat threshold history object.
            1. Data changes are implemented for the retrieved vat threshold history object

        CASE LATER (main case): The update's valid_from attribute is LATER than the currently valid vat threshold history object.
            1. New vat threshold history is created
            2. Current vat threshold history retrieved
            3. Missing data change attributes complemented by those from vat threshold history
            4. Current vat threshold history valid_to == new vat threshold history valid_from - timedelta(days=1)

        """

        # Trying to retrieve vat_threshold history to decide case
        valid_from = data_changes['valid_from']
        vat_threshold_history = VatThresholdHistoryService.get_by_vat_threshold_id_date(vat_threshold_id, valid_from)

        # CASE EARLIER
        if not isinstance(vat_threshold_history, VatThresholdHistory):
            #1.
            new_vat_threshold_history = VatThresholdHistory(vat_threshold_id=vat_threshold_id)
            db.session.add(new_vat_threshold_history)
            #2.
            vat_threshold_history = VatThresholdHistoryService.get_oldest(vat_threshold_id)
            #3. and #4.
            all_attr = {**vat_threshold_history.attr_as_dict(), **data_changes}
            all_attr['valid_to'] = vat_threshold_history.valid_from - timedelta(days=1)
            for key, val in all_attr.vat_thresholds():
                setattr(new_vat_threshold_history, key, val)

        else:
            # CASE EQUAL
            if valid_from == vat_threshold_history.valid_from:
                for key, val in data_changes.vat_thresholds():
                    setattr(vat_threshold_history, key, val)

            # CASE LATER
            else:
                vat_threshold_history = VatThresholdHistoryService.get_current(vat_threshold_id)
                #1.
                new_vat_threshold_history = VatThresholdHistory(vat_threshold_id=vat_threshold_id)
                db.session.add(new_vat_threshold_history)
                #(2.) -> already exists
                #3.
                all_attr = {**vat_threshold_history.attr_as_dict(), **data_changes}
                all_attr['valid_from'] = valid_from

                for key, val in all_attr.vat_thresholds():
                    setattr(new_vat_threshold_history, key, val)

                #4.
                vat_threshold_history.valid_to = valid_from - timedelta(days=1)



    @staticmethod
    def get_oldest(vat_threshold_id: int) -> VatThresholdHistory:
        return VatThresholdHistory.query.filter_by(vat_threshold_id=vat_threshold_id).order_by(VatThresholdHistory.valid_from.asc()).first()

    @staticmethod
    def get_current(vat_threshold_id: int) -> VatThresholdHistory:
        return VatThresholdHistory.query.filter_by(vat_threshold_id=vat_threshold_id).order_by(VatThresholdHistory.valid_from.desc()).first()

    @staticmethod
    def get_by_vat_threshold_id_date(vat_threshold_id: int, date: date):
        return VatThresholdHistory.query.filter(
            VatThresholdHistory.vat_threshold_id == vat_threshold_id,
            VatThresholdHistory.valid_from <= date,
            VatThresholdHistory.valid_to >= date
            ).first()

    @staticmethod
    def create(vat_threshold_data) -> VatThresholdHistory:

        # create new vat_threshold history
        new_vat_threshold_history = VatThresholdHistory(
            vat_threshold_id=vat_threshold_data.get('vat_threshold_id'),
            valid_from=vat_threshold_data.get('valid_from'),
            valid_to=vat_threshold_data.get('valid_to'),

            # mirrored attributes (no relationships)
            created_by = vat_threshold_data.get('created_by'),
            country_code = vat_threshold_data.get('country_code'),
            value = vat_threshold_data.get('value'),
            currency_code = vat_threshold_data.get('currency_code')
        )

        db.session.add(new_vat_threshold_history)
        db.session.commit()

        return new_vat_threshold_history
