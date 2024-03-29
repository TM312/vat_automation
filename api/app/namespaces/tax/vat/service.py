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
        if isinstance(vat, Vat):
            vat.update(data_changes)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

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
    def get_oldest(vat_id: int) -> VatHistory:
        return VatHistory.query.filter_by(vat_id=vat_id).order_by(VatHistory.valid_from.asc()).first()

    @staticmethod
    def get_current(vat_id: int) -> VatHistory:
        return VatHistory.query.filter_by(vat_id=vat_id).order_by(VatHistory.valid_from.desc()).first()


    @staticmethod
    def get_by_relationship_date(vat_id: int, date: date) -> VatHistory:
        return VatHistory.query.filter(
            VatHistory.vat_id == vat_id,
            VatHistory.valid_from <= date,
            VatHistory.valid_to >= date
        ).first()

    @staticmethod
    def create_empty(vat_id: int) -> VatHistory:
        # create new vat history
        new_vat_history = VatHistory(vat_id=vat_id)
        db.session.add(new_vat_history)
        db.session.commit()

        return new_vat_history

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
