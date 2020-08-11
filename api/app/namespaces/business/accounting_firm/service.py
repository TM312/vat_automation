from typing import List, Dict

from werkzeug.exceptions import Conflict, NotFound, Unauthorized
from uuid import UUID

from app.extensions import db
from .model import AccountingFirm

from typing import Dict

from .interface import AccountingFirmInterface

from ...user.tax_auditor.model import TaxAuditor


class AccountingFirmService:
    @staticmethod
    def get_all() -> List[AccountingFirm]:
        accounting_firms = AccountingFirm.query.all()
        return accounting_firms

    @staticmethod
    def get_by_public_id(public_id: str) -> AccountingFirm:
        return AccountingFirm.query.filter_by(public_id=public_id).first()

    @staticmethod
    def get_by_id(accounting_firm_id: str) -> AccountingFirm:
        return AccountingFirm.query.filter_by(id=accounting_firm_id).first()

    @staticmethod
    def update(accounting_firm_id: int, data_changes: AccountingFirmInterface) -> AccountingFirm:
        accounting_firm = AccountingFirmService.get_by_id(accounting_firm_id)
        accounting_firm.update(data_changes)
        db.session.commit()
        return accounting_firm


    @staticmethod
    def delete_by_public_id(accounting_firm_public_id: str) -> Dict:
        #check if accounting business exists in db
        accounting_firm = AccountingFirm.query.filter_by(public_id=accounting_firm_public_id).first()
        if accounting_firm:
            db.session.delete(accounting_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller firm (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')

    @staticmethod
    def delete_by_id(accounting_firm_id: int) -> Dict:
        #check if accounting business exists in db
        accounting_firm = AccountingFirm.query.filter_by(id=accounting_firm_id).first()
        if accounting_firm:
            db.session.delete(accounting_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Seller firm (Public ID: {}) has been successfully deleted.'.format(public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')



    @staticmethod
    def get_own(tax_auditor: TaxAuditor) -> AccountingFirm:
        #check if accounting_firm exists by querying the Business table for the tax_auditors employer id
        accounting_firm = AccountingFirm.query.filter(AccountingFirm.id == tax_auditor.employer.id).first()
        if accounting_firm:
            return accounting_firm
        else:
            raise NotFound('This accounting firm does not exist.')

    @staticmethod
    def update_own(tax_auditor: TaxAuditor, data_changes: AccountingFirmInterface) -> AccountingFirm:
        #check if accounting_firm exists by querying the Business table for the tax_auditors employer id
        accounting_firm = AccountingFirm.query.filter(AccountingFirm.id == tax_auditor.employer.id).first()
        if accounting_firm:
            accounting_firm.update(data_changes)
            db.session.commit()
            return accounting_firm
        else:
            raise NotFound('This accounting firm does not exist.')


    @staticmethod
    def delete_own(tax_auditor: TaxAuditor) -> Dict:
        #check if accounting_firm exists by querying the Business table for the tax_auditors employer id
        accounting_firm = AccountingFirm.query.filter(
            AccountingFirm.id == tax_auditor.employer.id).first()
        if accounting_firm:
            db.session.delete(accounting_firm)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Accounting firm (Public ID: {}) has been successfully deleted.'.format(accounting_firm.public_id)
            }
            return response_object
        else:
            raise NotFound('This accounting firm does not exist.')
