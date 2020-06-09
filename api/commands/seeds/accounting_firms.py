from app.namespaces.business.accounting_firm.model import AccountingFirm
from app.namespaces.user.tax_auditor.model import TaxAuditor
from app.extensions import db

class AccountingFirmSeedService:

    @staticmethod
    def seed_accounting_firm():
        accounting_firm_gvc = AccountingFirm(
            name = 'Global VAT Compliance',
            address = 'Loire 192, 2491 AM Den Haag, Netherlands'
        )
        db.session.add(accounting_firm_gvc)
        db.session.commit()

    @staticmethod
    def append_tax_auditor_to_accounting_firm():
        gvc = AccountingFirm.query.filter_by(name='Global VAT Compliance').first()
        gvc_main = TaxAuditor.query.filter_by(name='GVC Main').first()
        if not isinstance(gvc, AccountingFirm) or not isinstance(gvc_main, TaxAuditor):
            raise

        else:
            gvc.employees.append(gvc_main)
