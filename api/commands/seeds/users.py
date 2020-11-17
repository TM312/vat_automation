

from app.namespaces.user.admin import Admin
from app.namespaces.user.tax_auditor import TaxAuditor
from app.namespaces.user.seller import Seller
from app.namespaces.user.seller.service import SellerService

from app.namespaces.business.accounting_firm import AccountingFirm
from app.namespaces.business.seller_firm import SellerFirm

from app.extensions import db


class AdminSeedService:
    @staticmethod
    def seed_admin():
        new_admin = Admin(
            name = 'Thomas M.',
            email = 'thomas.moellers@rwth-aachen.de',
            password = 'ch_ch_ch_check',
            role = 'zzz'
        )
        db.session.add(new_admin)
        db.session.commit()

    @staticmethod
    def append_accounting_firm_to_admin():
        thomas = Admin.query.filter_by(name='Thomas M.').first()
        testAF = AccountingFirm.query.filter_by(name='Test Accounting Firm').first()

        thomas.created_businesses.append(testAF)


class TaxAuditorSeedService:
    @staticmethod
    def seed_tax_auditor():
        test_firm_auditor = TaxAuditor( name='Test User Main', email='test_ta_main@mail.com', password='another_d3y_4NothR_p4$$w_ord', role='admin')
        db.session.add(test_firm_auditor)

        test_firm_auditor_1 = TaxAuditor( name='Test Tax Auditor 1', email='test_tax_auditor1@mail.com', password='another_d3y_4NothR_p4$$w_ord', role='tax_auditor')
        db.session.add(test_firm_auditor_1)

        test_firm_auditor_2 = TaxAuditor( name='Test Tax Auditor 2', email='test_tax_auditor2@mail.com', password='another_d3y_4NothR_p4$$w_ord', role='tax_auditor')
        db.session.add(test_firm_auditor_2)

        test_firm_auditor_3 = TaxAuditor( name='Test Tax Auditor 3', email='test_tax_auditor3@mail.com', password='another_d3y_4NothR_p4$$w_ord', role='tax_auditor')
        db.session.add(test_firm_auditor_3)

        db.session.commit()


class SellerSeedService:
    @staticmethod
    def seed_seller():
        new_seller = Seller(
            name='James B.',
            email='james.b@mi6-mail.com',
            password='ch_ch_ch_check',
            role='007'
        )
        db.session.add(new_seller)
        db.session.commit()

    @staticmethod
    def append_seller_firm_to_seller():

        james = SellerService.get_by_email('james.b@mi6-mail.com')
        bond_store = SellerFirm.query.filter_by(name='Bond Store Ltd').first()

        james.created_businesses.append(bond_store)
