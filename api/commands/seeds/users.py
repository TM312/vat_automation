

from app.namespaces.user.admin import Admin
from app.namespaces.user.tax_auditor import TaxAuditor
from app.namespaces.business.accounting_firm import AccountingFirm

from app.extensions import db


class AdminSeedService:
    @staticmethod
    def seed_admin():
        new_admin = Admin(
            name = 'Thomas M.',
            email = 'thomas.moellers@rwth-aachen.de',
            password = '21358***',
            role = 'boss',
        )
        db.session.add(new_admin)
        db.session.commit()

    @staticmethod
    def append_accounting_firm_to_admin():
        thomas = Admin.query.filter_by(name='Thomas M.').first()
        gvc = AccountingFirm.query.filter_by(name='Global VAT Compliance').first()
        if not isinstance(gvc, AccountingFirm) or not isinstance(thomas, Admin):
            raise

        else:
            thomas.created_businesses.append(gvc)


class TaxAuditorSeedService:
    @staticmethod
    def seed_tax_auditor():
        new_tax_auditor = TaxAuditor(
            name = 'GVC Main',
            email = 'thomas.moellers@unisg.ch',
            password = 'change_once_in_use',
            role = 'admin',
        )
        db.session.add(new_tax_auditor)

        new_tax_auditor1 = TaxAuditor(
            name='GVC Tax Auditor 1',
            email='gvc_tax_auditor1@mail.com',
            password='change_once_in_use',
            role='tax_auditor',
        )
        db.session.add(new_tax_auditor1)

        new_tax_auditor2 = TaxAuditor(
            name='GVC Tax Auditor 2',
            email='gvc_tax_auditor2@mail.com',
            password='change_once_in_use',
            role='tax_auditor',
        )
        db.session.add(new_tax_auditor2)

        new_tax_auditor3 = TaxAuditor(
            name='GVC Tax Auditor 3',
            email='gvc_tax_auditor3@mail.com',
            password='change_once_in_use',
            role='tax_auditor',
        )
        db.session.add(new_tax_auditor3)


        db.session.commit()
