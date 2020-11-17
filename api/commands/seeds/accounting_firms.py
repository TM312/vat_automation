from app.namespaces.business.accounting_firm import AccountingFirm
from app.namespaces.user.tax_auditor import TaxAuditor
from app.extensions import db

class AccountingFirmSeedService:

    @staticmethod
    def seed_accounting_firm():

        accounting_firm_test = AccountingFirm(
            name='Test Accounting Firm',
            address='Test Address'
        )
        db.session.add(accounting_firm_test)


        db.session.commit()

    @staticmethod
    def append_tax_auditor_to_accounting_firm():

        test = AccountingFirm.query.filter_by(name='Test Accounting Firm').first()

        test_firm_auditor = TaxAuditor.query.filter_by(name = 'Test User Main').first()
        test_firm_auditor_1 = TaxAuditor.query.filter_by(name = 'Test Tax Auditor 1').first()
        test_firm_auditor_2 = TaxAuditor.query.filter_by(name = 'Test Tax Auditor 2').first()
        test_firm_auditor_3 = TaxAuditor.query.filter_by(name = 'Test Tax Auditor 3').first()

        test_all = [
            test_firm_auditor,
            test_firm_auditor_1,
            test_firm_auditor_2,
            test_firm_auditor_3
        ]

        # if not isinstance(gvc, AccountingFirm):
        #     raise

        # else:
        # for tax_auditor in gvc_all:
        #     gvc.employees.append(tax_auditor)

        for tax_auditor in test_all:
            test.employees.append(tax_auditor)
