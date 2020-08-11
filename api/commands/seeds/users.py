

from app.namespaces.user.admin import Admin
from app.namespaces.user.tax_auditor import TaxAuditor
from app.namespaces.business.accounting_firm import AccountingFirm

from app.extensions import db


class AdminSeedService:
    @staticmethod
    def seed_admin():
        new_admin = Admin(
            name = 'Thomas M.',
            email = 'tm@mail.de',
            password = 'ch_ch_ch_check',
            role = 'zzz'
        )
        db.session.add(new_admin)

        new_admin2 = Admin(
            name='Nico P.',
            email='nico@email.com',
            password='check_the_mic',
            role='employee'
        )
        db.session.add(new_admin2)
        db.session.commit()

    @staticmethod
    def append_accounting_firm_to_admin():
        thomas = Admin.query.filter_by(name='Thomas M.').first()
        gvc = AccountingFirm.query.filter_by(name='Global VAT Compliance').first()
        testAF = AccountingFirm.query.filter_by(name='Test Accounting Firm').first()

        if not isinstance(gvc, AccountingFirm) or not isinstance(testAF, AccountingFirm) or not isinstance(thomas, Admin):
            raise

        else:
            thomas.created_businesses.append(gvc)
            thomas.created_businesses.append(testAF)


class TaxAuditorSeedService:
    @staticmethod
    def seed_tax_auditor():
        new_tax_auditor = TaxAuditor( name = 'GVC Main', email = 'gvc_main@mail.com', password = 'change_once_in_use', role = 'admin')
        db.session.add(new_tax_auditor)

        new_tax_auditor1 = TaxAuditor( name='GVC Tax Auditor 1', email='gvc_tax_auditor1@mail.com', password='change_once_in_use', role='tax_auditor')
        db.session.add(new_tax_auditor1)

        new_tax_auditor2 = TaxAuditor( name='GVC Tax Auditor 2', email='gvc_tax_auditor2@mail.com', password='change_once_in_use', role='tax_auditor')
        db.session.add(new_tax_auditor2)

        new_tax_auditor3 = TaxAuditor( name='GVC Tax Auditor 3', email='gvc_tax_auditor3@mail.com', password='change_once_in_use', role='tax_auditor')
        db.session.add(new_tax_auditor3)

        test_firm_auditor = TaxAuditor( name='Test User Main', email='test_ta_main@mail.com', password='change_once_in_use', role='admin')
        db.session.add(test_firm_auditor)

        test_firm_auditor_1 = TaxAuditor( name='Test Tax Auditor 1', email='test_tax_auditor1@mail.com', password='change_once_in_use', role='tax_auditor')
        db.session.add(test_firm_auditor_1)

        test_firm_auditor_2 = TaxAuditor( name='Test Tax Auditor 2', email='test_tax_auditor2@mail.com', password='change_once_in_use', role='tax_auditor')
        db.session.add(test_firm_auditor_2)

        test_firm_auditor_3 = TaxAuditor( name='Test Tax Auditor 3', email='test_tax_auditor3@mail.com', password='change_once_in_use', role='tax_auditor')
        db.session.add(test_firm_auditor_3)

        db.session.commit()
