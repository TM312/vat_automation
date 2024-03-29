from typing import List
import pandas as pd

from app.extensions import db
from flask import current_app, g

from .model import TaxAuditor
from .interface import TaxAuditorInterface



class TaxAuditorService:

    @staticmethod
    def get_all() -> List[TaxAuditor]:
        tax_auditors = TaxAuditor.query.all()
        return tax_auditors


    @staticmethod
    def get_by_id(tax_auditor_id: int) -> TaxAuditor:
        return TaxAuditor.query.filter_by(id = tax_auditor_id).first()

    @staticmethod
    def get_by_public_id(tax_auditor_public_id: str) -> TaxAuditor:
        return TaxAuditor.query.filter_by(public_id=tax_auditor_public_id).first()



    @staticmethod
    def create(tax_auditor_data: TaxAuditorInterface) -> TaxAuditor:
        new_tax_auditor = TaxAuditor(
            name = tax_auditor_data.get('name'),
            email = tax_auditor_data.get('email'),
            employer_id = tax_auditor_data.get('employer_id'),
            role = tax_auditor_data.get('role'),
            password = tax_auditor_data.get('password'),
            location = tax_auditor_data.get('location')
        )

        db.session.add(new_tax_auditor)
        db.session.commit()

        return new_tax_auditor

    @staticmethod
    def update(tax_auditor_id: int, data_changes) -> TaxAuditor:
        tax_auditor = TaxAuditorService.get_by_id(tax_auditor_id)
        tax_auditor.update(data_changes)
        tax_auditor.update_last_seen()
        db.session.commit()
        return tax_auditor


    @staticmethod
    def delete_by_public_id(tax_auditor_public_id: str):
        #check if tax_auditor exists in db
        tax_auditor = TaxAuditorService.get_by_public_id(tax_auditor_public_id)
        if tax_auditor:
            db.session.delete(tax_auditor)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Tax auditor (Public ID: {}) has been successfully deleted.'.format(tax_auditor_public_id)
            }
            return response_object
        else:
            raise NotFound('This tax auditor does not exist.')


    @staticmethod
    def append_delete_seller_firm_to_key_accounts(seller_firm_public_id: str) -> TaxAuditor:
        from app.namespaces.business.seller_firm.service import SellerFirmService
        seller_firm = SellerFirmService.get_by_public_id(seller_firm_public_id)
        if seller_firm:
            if seller_firm in g.user.key_accounts:
                g.user.key_accounts.remove(seller_firm)
            else:
                g.user.key_accounts.append(seller_firm)

            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

        return g.user
