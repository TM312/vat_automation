from app.namespaces.business.accounting_firm import AccountingFirm
from app.namespaces.business.seller_firm import SellerFirm
from app.namespaces.user.tax_auditor import TaxAuditor
from app.extensions import db

class SellerFirmSeedService:

    @staticmethod
    def seed_sample_seller_firm():

        sample_seller_firm = SellerFirm(
            name='Bond Store Ltd',
            address="37–38 St James's Street, London",
            establishment_country_code='GB'
        )
        db.session.add(sample_seller_firm)


        db.session.commit()

    @staticmethod
    def append_accounting_firm_to_seller_firm():
        testAF = AccountingFirm.query.filter_by(name='Test Accounting Firm').first()
        bondSF = SellerFirm.query.filter_by(name='Bond Store Ltd').first()

        testAF.clients.append(bondSF)
