from typing import List

from werkzeug.exceptions import Conflict, NotFound, Unauthorized

from app.extensions import db
from .model import AccountingFirm
from .schema import accounting_firm_dto

from typing import Dict

from .interface import AccountingFirmInterface

from ...user.tax_auditor.model import TaxAuditor
from ...utils.schema import response_object_dto


class AccountingFirmService:
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
    def delete_own(tax_auditor: TaxAuditor) -> response_object_dto:
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
