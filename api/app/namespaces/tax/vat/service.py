from datetime import date
from typing import List

from werkzeug.exceptions import NotFound
from app.extensions import db


from . import Vat, VatHistory
from .interface import VatInterface
from app.namespaces.utils.service import NotificationService



class VatService:
    @staticmethod
    def get_all() -> List[Vat]:
        vats = Vat.query.all()
        return vats

    @staticmethod
    def get_by_id(vat_id: int) -> Vat:
        return Vat.query.filter_by(id=vat_id).first()

    @staticmethod
    def get_by_country_tax_rate_type(country_code: str, tax_rate_type_code: str) -> List[Vat]:
        return Vat.query.filter(Vat.country_code == country_code, Vat.tax_rate_type_code == tax_rate_type_code).all()

    @staticmethod
    def get_by_country_code(country_code: str) -> List[Vat]:
        return Vat.query.filter_by(country_code = country_code).all()

    @staticmethod
    def get_by_tax_code(tax_code_code: str) -> List[Vat]:
        return Vat.query.filter_by(tax_code_code=tax_code_code).all()


    @staticmethod
    def update(vat_id: int, data_changes: VatInterface) -> Vat:
        vat = VatService.get_by_id(vat_id)
        vat.update(data_changes)
        db.session.commit()
        return vat

    @staticmethod
    def delete_by_id(vat_id: int):
        vat = VatService.get_by_id(vat_id)
        if vat:
            db.session.delete(vat)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Vat (id: {}) has been successfully deleted.'.format(vat_id)
            }
            return response_object
        else:
            raise NotFound('This vat does not exist.')

    @staticmethod
    def create(vat_data: VatInterface) -> Vat:

        new_vat = Vat(
            country_code = vat_data.get('country_code'),
            tax_code_code = vat_data.get('tax_code_code'),
            tax_rate_type_code = vat_data.get('tax_rate_type_code'),
            rate = vat_data.get('rate')
        )

        #add vat to db
        db.session.add(new_vat)
        db.session.commit()

        vat_data['vat_id'] = new_vat.id
        try:
            VatHistoryService.create(vat_data)
        except:
            db.session.rollback()
            raise

        return new_vat



class VatHistoryService:

    @staticmethod
    def get_by_tax_code_country_tax_date(tax_code_code: str, country_code: str, tax_date: date) -> VatHistory:
        return VatHistory.query.filter(
            VatHistory.tax_code_code==tax_code_code,
            VatHistory.country_code==country_code,
            VatHistory.valid_from<=tax_date,
            VatHistory.valid_to>=tax_date
            ).first()


    @staticmethod
    def get_by_tax_rate_type_country_tax_date(country_code: str, tax_rate_type_code: str, tax_date: date) -> VatHistory:
        return VatHistory.query.filter(
            VatHistory.country_code==country_code,
            VatHistory.tax_rate_type_code==tax_rate_type_code,
            VatHistory.valid_from<=tax_date,
            VatHistory.valid_to>=tax_date
            ).first()

    @staticmethod
    def handle_update(vat_id, data_changes):
        """
        When updating 3 cases can exist:

        CASE EARLIER: The update's valid_from attribute is EARLIER than any other history object.
            1. New history object is created
            2. Oldest history object retrieved
            3. Missing data change attributes complemented by those from oldest history object
            4. New history object valid_to == oldest history object valid_from - timedelta(days=1)

        CASE EQUAL: The update's valid_from attribute is EQUAL to another history object.
            1. Data changes are implemented for the retrieved history object

        CASE LATER (main case): The update's valid_from attribute is LATER than the currently valid history object.
            1. New history object is created
            2. Current history object retrieved
            3. Missing data change attributes complemented by those from history object
            4. Current history object valid_to == new history object valid_from - timedelta(days=1)

        """

        # Trying to retrieve item history to decide case
        valid_from = data_changes['valid_from']
        vat_history = VatHistoryService.get_by_vat_id_date(vat_id, valid_from)


        # CASE EARLIER
        if not isinstance(vat_history, VatHistory):
            #1.
            new_vat_history = VatHistory(vat_id=vat_id)
            db.session.add(new_vat_history)
            #2.
            vat_history = VatHistoryService.get_oldest(vat_id)
            #3. and #4.
            all_attr = {**vat_history.attr_as_dict(), **data_changes}
            all_attr['valid_to'] = vat_history.valid_from - timedelta(days=1)
            for key, val in all_attr.items():
                setattr(new_vat_history, key, val)

        else:
            # CASE EQUAL
            if valid_from == vat_history.valid_from:
                for key, val in data_changes.items():
                    setattr(vat_history, key, val)

            # CASE LATER
            else:
                vat_history = VatHistoryService.get_current(vat_id)

                #1.
                new_vat_history = VatHistory(vat_id=vat_id)
                db.session.add(new_vat_history)
                #(2.) -> already exists
                #3.
                all_attr = {**vat_history.attr_as_dict(), **data_changes}

                for key, val in all_attr.items():
                    setattr(new_vat_history, key, val)

                #4.
                vat_history.valid_to = valid_from - timedelta(days=1)



    @staticmethod
    def get_oldest(vat_id: int) -> VatHistory:
        return VatHistory.query.filter_by(vat_id=vat_id).order_by(VatHistory.valid_from.asc()).first()

    @staticmethod
    def get_current(vat_id: int) -> VatHistory:
        return VatHistory.query.filter_by(vat_id=vat_id).order_by(VatHistory.valid_from.desc()).first()


    @staticmethod
    def get_by_vat_id_date(vat_id: int, date: date) -> VatHistory:
        return VatHistory.query.filter(
            VatHistory.vat_id == vat_id,
            VatHistory.valid_from <= date,
            VatHistory.valid_to >= date
        ).first()


    @staticmethod
    def create(vat_data) -> VatHistory:

        # create new vat history
        new_vat_history = VatHistory(
            vat_id=vat_data.get('vat_id'),
            valid_from=vat_data.get('valid_from'),
            valid_to=vat_data.get('valid_to'),

            # mirrored attributes (no relationships)
            country_code=vat_data.get('country_code'),
            tax_code_code=vat_data.get('tax_code_code'),
            tax_rate_type_code=vat_data.get('tax_rate_type_code'),
            comment = vat_data.get('comment'),
            rate=vat_data.get('rate')
        )

        db.session.add(new_vat_history)
        db.session.commit()

        return new_vat_history


    @staticmethod
    def compare_reference_calculated_vat_rates(transaction_id: int, transaction_input: 'app.namespaces.transaction_input.TransactionInput', reference_vat_rate: float, calculated_vat_rate: float):

        if reference_vat_rate != calculated_vat_rate:
            notification_data = NotificationService.create_transaction_notification_data(
                main_subject='Tax Rate',
                original_filename=transaction_input.original_filename,
                status='warning',
                reference_value=str(reference_vat_rate),
                calculated_value=str(calculated_vat_rate),
                transaction_id=transaction_id
            )
            try:
                NotificationService.create_transaction_notification(notification_data)
            except:
                db.session.rollback()
                raise
