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

        accounting_firm_test = AccountingFirm(
            name='Test Accounting Firm',
            address='Test Address'
        )
        db.session.add(accounting_firm_test)


        db.session.commit()

    @staticmethod
    def append_tax_auditor_to_accounting_firm():
        gvc = AccountingFirm.query.filter_by(name='Global VAT Compliance').first()

        tax_auditor_gvc_main = TaxAuditor.query.filter_by(name = 'GVC Main').first()
        tax_auditor_gvc_1 = TaxAuditor.query.filter_by(name = 'GVC Tax Auditor 1').first()
        tax_auditor_gvc_2 = TaxAuditor.query.filter_by(name = 'GVC Tax Auditor 2').first()
        tax_auditor_gvc_3 = TaxAuditor.query.filter_by(name = 'GVC Tax Auditor 3').first()

        gvc_all = [
            tax_auditor_gvc_main,
            tax_auditor_gvc_1,
            tax_auditor_gvc_2,
            tax_auditor_gvc_3
        ]

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

        if not isinstance(gvc, AccountingFirm):
            raise

        else:
            for tax_auditor in gvc_all:
                gvc.employees.append(tax_auditor)

            for tax_auditor in test_all:
                test.employees.append(tax_auditor)
