from datetime import date
from typing import List
from werkzeug.exceptions import NotFound

from . import Vat
from .interface import VatInterface
from ...utils.service import NotificationService



class VatService:
    @staticmethod
    def get_all() -> List[Vat]:
        vats = Vat.query.all()
        return vats

    @staticmethod
    def get_by_id(vat_id: int) -> Vat:
        return Vat.query.filter(Vat.code == code).first()

    @staticmethod
    def update(vat_id: int, data_changes: VatInterface) -> Vat:
        vat = VatService.get_by_id(codvat_ide)
        vat.update(data_changes)
        db.session.commit()
        return vat

    @staticmethod
    def delete_by_id(vat_id: str):
        vat = Vat.query.filter(Vat.id == vat_id).first()
        if vat:
            db.session.delete(vat)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Vat (code: {}) has been successfully deleted.'.format(vat_id)
            }
            return response_object
        else:
            raise NotFound('This vat does not exist.')

    @staticmethod
    def create(vat_data: VatInterface) -> Vat:

        new_vat = Vat(
            valid_from = vat_data.get('valid_from'),
            valid_to = vat_data.get('valid_to'),
            country_code = vat_data.get('country_code'),
            tax_code_code = vat_data.get('tax_code_code'),
            tax_rate_type_code = vat_data.get('tax_rate_type_code'),
            rate = vat_data.get('rate')
        )

        #add seller firm to db
        db.session.add(new_vat)
        db.session.commit()

        return new_vat



    @staticmethod
    def get_by_tax_code_country_tax_date(tax_code_code: str, country: 'app.namespaces.country.Country', tax_date: date) -> Vat:
        vat = Vat.query.filter(Vat.tax_code_code==tax_code_code, Vat.country==country, Vat.valid_from<=tax_date, Vat.valid_to>=tax_date).first()
        if vat:
            return vat
        else:
            raise NotFound('The tax rate for the tax code: "{}" and the country: "{}" could not be found. Please get in contact with one of the admins.'.format(tax_code, country.name))

    @staticmethod
    def get_by_tax_rate_type_country_tax_date(country: 'app.namespaces.country.Country', tax_rate_type_code: str, tax_date: date) -> Vat:
        vat: Vat = Vat.query.filter(Vat.country==country, Vat.tax_rate_type_code==tax_rate_type_code, Vat.valid_from<=tax_date, Vat.valid_to>=tax_date).first()
        if vat:
            return vat
        else:
            raise NotFound('The tax rate for the tax rate type "{}" and the country "{}" could not be found. Please get in contact with one of the admins.'.format(tax_rate_type_code, country.name))

    @staticmethod
    def compare_reference_calculated_vat_rates(transaction_id: int, transaction_input: 'app.namespaces.transaction_input.TransactionInput', reference_vat_rate: float, calculated_vat_rate: float):

        if reference_vat_rate != calculated_vat_rate:
            notification_data = NotificationService.create_notification_data(
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
