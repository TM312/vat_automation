from app.namespaces.business.accounting_firm import AccountingFirm
from app.namespaces.user.tax_auditor import TaxAuditor
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
        gvc_all = TaxAuditor.query.all()
        if not isinstance(gvc, AccountingFirm):
            raise

        else:
            for tax_auditor in gvc_all:
                gvc.employees.append(tax_auditor)
